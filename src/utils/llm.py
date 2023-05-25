"""Functions for interacting with the OpenAI Language Model (LLM)."""


import os
import yaml
import time
import re

import tiktoken
import openai

from prompt_templates.system_message import system_message_template
from utils.log import log


def prompt_to_respond_with_yaml() -> str:
    return """Reply with only the file contents enclosed by the strings "<file contents>" and "</file contents>"."""


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
    - The contents of an updated file which addresses the suggested improvements enclosed by the strings "<file contents>" and "</file contents>"."""


def parse_single_file_contents(markdown: str) -> str:
    pattern = r"<file contents>(.*?)</file contents>"
    matches = re.findall(pattern, markdown, re.DOTALL)
    assert len(matches) == 1, f"Expected 1 block of file contents in the response, found {len(matches)}."
    return matches[0]


def parse_single_file_improvements(markdown: str) -> str:
    pattern = r"<improvements>(.*?)</improvements>"
    matches = re.findall(pattern, markdown, re.DOTALL)
    assert len(matches) == 1, f"Expected 1 block of improvements in the response, found {len(matches)}."
    return matches[0]


def serialize_file_contents(file_contents: str) -> str:
    return f"<file contents>{file_contents}</file contents>"


def query_llm(
        message: str, 
        max_request_attempts: int = 3,
        # openai_model: str = "gpt-3.5-turbo",
        openai_model: str = "gpt-4-0314", 
        stream_response: bool = False,
        tokens_per_log_msg: int = 100
    ) -> str | None:
    """Send the system message and design message to OpenAI and return the reply."""
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
    attempts = 1
    while attempts < max_request_attempts:
        try:
            response = openai.ChatCompletion.create(stream=stream_response, **params)
            if stream_response:
                total_tokens_recieved_so_far = 0
                last_log_msg_token_count = 0
                reply = ""
                request_start_time = time.time()
                for chunk in response:
                    content = chunk["choices"][0].get("delta", {}).get("content")
                    if content is not None:
                        reply += content
                        total_tokens_recieved_so_far += len(encoding.encode(content))
                        if total_tokens_recieved_so_far - last_log_msg_token_count >= tokens_per_log_msg:
                            log.debug(f"Recieving response... (total tokens recieved so far: {total_tokens_recieved_so_far}; "
                                    f"total elapsed time: {time.time() - request_start_time:.2f} seconds)")
                            last_log_msg_token_count = total_tokens_recieved_so_far
            else:
                reply = response.choices[0]["message"]["content"]
                log.info(f"Response time: {response.response_ms / 1000. / 60.:.2f} minutes")
                log.info(f"Tokens (Prompt, Completion, Total): "
                        f"({response.usage['prompt_tokens']}, "
                        f"{response.usage['completion_tokens']}, "
                        f"{response.usage['total_tokens']})")
            log.debug(f"llm reply:\n{reply}")
            break
        except [openai.error.RateLimitError, openai.error.APIError] as err:
            log.warning(f"OpenAI rate limit error ({err}). This was attempt {attempts} of {max_request_attempts}.")
            reply = None
        attempts += 1
    return reply


def send_templated_message_to_llm(message: str, max_improvement_iterations: int = 0) -> tuple[str, str]:
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
        reflection_instruction = f"{system_message}\n{prompt_to_reflect_and_improve(original_instructions, reply_without_improvements)}"
        reply = query_llm(f"{system_message}\n{reflection_instruction}")
        if "No improvements need to be made." in reply:
            log.info("No improvements need to be made.")
            break
        parsed_file_contents = parse_single_file_contents(reply)
        log.info(f"Needed improvements:\n{parse_single_file_improvements(reply)}")
        improvement_iters += 1

    return parsed_file_contents
