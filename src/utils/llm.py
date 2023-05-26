"""Functions for interacting with the OpenAI Language Model (LLM)."""


import os
import time
import re

import requests
import tiktoken
import openai

from prompt_templates.system_message import system_message_template
from utils.log import log


def prompt_to_respond_with_yaml() -> str:
    return """Reply with only the file contents directly enclosed by the strings "<file_contents>" and "</file_contents>" without any surrounding markdown code block syntax."""


def prompt_to_reflect_and_improve(message: str, reply: str) -> str:
    return f"""Given the request from the user:
{message}

The following response was returned:
{reply}

Your instructions:
- Suggest improvements you think should be made to the response so that the response fully addresses the request from the user.
- It is important that the response clearly and in great detail addresses the request from the user. 
- If you do not have any suggested improvements to the response, only respond with the exact string `No improvements need to be made.` and nothing else.
- If you have suggested improvements, reply with:
    - A list of the suggested improvements enclosed by the strings "<improvements>" and "</improvements>".
    - The contents of an updated file which addresses the suggested improvements enclosed by the strings "<file_contents>" and "</file_contents>" without any surrounding markdown code block syntax."""


def parse_single_file_contents(markdown: str) -> str:
    pattern = r"<file[_ ]contents>\n(.*?)</file[_ ]contents>"
    matches = re.findall(pattern, markdown, re.DOTALL)
    assert len(matches) == 1, f"Expected 1 block of file contents in the response, found {len(matches)}."
    return matches[0]


def parse_single_file_improvements(markdown: str) -> str:
    pattern = r"<improvements>\n(.*?)</improvements>"
    matches = re.findall(pattern, markdown, re.DOTALL)
    assert len(matches) == 1, f"Expected 1 block of improvements in the response, found {len(matches)}."
    return matches[0]


def serialize_file_contents(file_contents: str) -> str:
    return f"<file_contents>\n{file_contents}</file_contents>"


def query_llm(
        message: str,
        max_request_attempts: int = 5,
        # openai_model: str = "gpt-3.5-turbo",
        openai_model: str = "gpt-4-0314",
        stream_response: bool = False,
        tokens_per_log_msg: int = 100
    ) -> str | None:
    """Send the a message to OpenAI and return the reply (with retries).
    
    Args:
        message: The message to send to OpenAI.
        max_request_attempts: The maximum number of attempts to make to send the request to OpenAI.
        openai_model: The OpenAI model to use.
        stream_response: Whether to stream the response from OpenAI.
        tokens_per_log_msg: The number of tokens to recieve before logging a message.
        
    Returns:
        The reply from OpenAI. If the request (including retries) fails, returns None."""
    openai.api_key = os.getenv("OPENAI_KEY")

    openai_model_max_tokens = 2048
    encoding = tiktoken.encoding_for_model(openai_model)

    log.debug(f"llm query:\n{message}")
    messages = []
    messages.append({"role": "user", "content": message})

    params = {
        "model": openai_model,
        "messages": messages,
        "max_tokens": openai_model_max_tokens,
        "temperature": 0
    }
    reply = None
    attempts = 1
    while reply is None and attempts <= max_request_attempts:
        try:
            response = openai.ChatCompletion.create(stream=stream_response, **params)
            if stream_response:
                total_tokens_recieved_so_far = 0
                last_log_msg_token_count = 0
                streamed_reply = ""
                request_start_time = time.time()
                for chunk in response:
                    content = chunk["choices"][0].get("delta", {}).get("content")
                    if content is not None:
                        streamed_reply += content
                        total_tokens_recieved_so_far += len(encoding.encode(content))
                        if total_tokens_recieved_so_far - last_log_msg_token_count >= tokens_per_log_msg:
                            log.debug(f"Recieving response... (total tokens recieved so far: {total_tokens_recieved_so_far}; "
                                    f"total elapsed time: {time.time() - request_start_time:.2f} seconds)")
                            last_log_msg_token_count = total_tokens_recieved_so_far
                reply = streamed_reply  # set this last, incase the API errors out mid-reply
            else:
                reply = response.choices[0]["message"]["content"]
                log.info(f"Response time: {response.response_ms / 1000. / 60.:.2f} minutes")
                log.info(f"Tokens (Prompt, Completion, Total): "
                        f"({response.usage['prompt_tokens']}, "
                        f"{response.usage['completion_tokens']}, "
                        f"{response.usage['total_tokens']})")
            log.debug(f"llm reply:\n{reply}")
        except openai.error.APIError as err:
            log.warning(f"OpenAI API returned an API Error: {err}. This was attempt {attempts} of {max_request_attempts}.")
        except openai.error.APIConnectionError as err:
            log.warning(f"Failed to connect to OpenAI API: {err}. This was attempt {attempts} of {max_request_attempts}.")
        except openai.error.RateLimitError as err:
            log.warning(f"OpenAI API request exceeded rate limit: {err}. This was attempt {attempts} of {max_request_attempts}.")
        except openai.error.Timeout as err:
            log.warning(f"OpenAI API request timed out: {err}. This was attempt {attempts} of {max_request_attempts}.")
        except openai.error.RateLimitError as err:
            log.warning(f"OpenAI API rate limit hit: {err}. This was attempt {attempts} of {max_request_attempts}.")
            log.warning("Sleeping for 60 seconds...")
            time.sleep(60)
        except requests.exceptions.ChunkedEncodingError as err:
            log.warning(f"OpenAI API request errored out: {err}. This was attempt {attempts} of {max_request_attempts}.")
        attempts += 1
    if reply is None:
        raise ValueError(f"Failed to get a reply from OpenAI after {max_request_attempts} attempts.")
    return reply


def send_templated_message_to_llm(message: str, max_improvement_iterations: int = 0) -> str:
    """Send a templated message to LLM and return the reply (with improvements).
    
    Args:
        message: The message to send to LLM.
        max_improvement_iterations: 
            The maximum number of times to attempt to improve the LLM's reply.
        
    Returns:
        The reply from LLM (with improvements)."""

    # Anecdotally, sending the system message as the system message (as opposed to just
    # including it in the user message) seems to work better.
    system_message = system_message_template()
    original_instructions = f"{message}\n{prompt_to_respond_with_yaml()}"
    reply = query_llm(f"{system_message}\n{original_instructions}")
    parsed_file_contents = parse_single_file_contents(reply)
    
    improvement_iters = 1
    needs_improvement = True
    while needs_improvement and improvement_iters <= max_improvement_iterations:
        log.debug(f"Reflective improvement attempt {improvement_iters} of {max_improvement_iterations}")
        reply_without_improvements = serialize_file_contents(parsed_file_contents)
        reflection_instruction = (
            f"{system_message}\n"
            f"{prompt_to_reflect_and_improve(original_instructions, reply_without_improvements)}")
        reply = query_llm(f"{system_message}\n{reflection_instruction}")
        if "No improvements need to be made." in reply:
            log.info("No improvements need to be made.")
            break
        parsed_file_contents = parse_single_file_contents(reply)
        log.info(f"Needed improvements:\n{parse_single_file_improvements(reply)}")
        improvement_iters += 1

    return parsed_file_contents
