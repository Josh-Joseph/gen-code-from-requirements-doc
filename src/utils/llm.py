"""Functions for interacting with the OpenAI Language Model (LLM)."""


import os
import yaml

import openai

from prompt_templates.system_message import system_message_template
from utils.log import log


def prompt_to_respond_with_yaml() -> str:
    return """Your reply should be formatted as a valid yaml file:
path_and_filename: <path_and_filename>
file_contents: <file_contents>
"""


def prompt_to_reflect_and_improve(message: str, reply: str) -> str:
    return f"""Given the request from the user:
{message}

The following response was returned:
{reply}

Suggest improvements you think should be made to the response so that the response fully addresses the request from the user. It is important that the response clearly and in great detail addresses the request from the user. 
If you do not have any suggested improvements to the response, just respond with 'No improvements need to be made.'
If you have suggested improvements, your reply should be formatted as a valid yaml file:
improvements: <improvements listed as a yaml sequence>
path_and_filename: <path_and_filename>
file_contents: <response which addresses the suggested improvements>'
"""



def query_llm(message: str, max_request_attempts: int = 3) -> str | None:
    """Send the system message and design message to OpenAI and return the reply."""
    openai.api_key = os.getenv("OPENAI_KEY")

    openai_model = "gpt-4-0314"
    openai_model_max_tokens = 2048

    log.debug(f"llm query:\n{message}")
    messages = []
    messages.append({"role": "user", "content": message})

    params = {
        "model": openai_model,
        "messages": messages,
        "max_tokens": openai_model_max_tokens,
        "temperature": 0,
    }
    attempts = 1
    while attempts < max_request_attempts:
        try:
            response = openai.ChatCompletion.create(**params)
            reply = response.choices[0]["message"]["content"]
            log.debug(f"llm reply:\n{reply}")
            log.info(f"Response time: {response.response_ms / 1000. / 60.:.2f} minutes")
            log.info(f"Tokens (Prompt, Completion, Total): "
                     f"({response.usage['prompt_tokens']}, "
                     f"{response.usage['completion_tokens']}, "
                     f"{response.usage['total_tokens']})")
            break
        except openai.error.RateLimitError:
            log.warning(f"OpenAI rate limit error (attempt {attempts} of {max_request_attempts})")
            reply = None
        attempts += 1
    return reply


def send_templated_message_to_llm(message: str, max_improvement_iterations: int = 0) -> tuple[str, str]:
    # Anecdotally, sending the system message as the system message (as opposed to just
    # including it in the user message) seems to work better.
    system_message = system_message_template()
    original_instructions = f"{message}\n{prompt_to_respond_with_yaml()}"
    reply = query_llm(f"{system_message}\n{original_instructions}")
    parsed_reply = yaml.safe_load(reply)
    
    improvement_iters = 1
    needs_improvement = True
    while needs_improvement and improvement_iters <= max_improvement_iterations:
        log.debug(f"Reflective improvement attempt {improvement_iters} of {max_improvement_iterations}")
        reply_without_improvements = yaml.safe_dump({k: parsed_reply[k] for k in ["path_and_filename", "file_contents"]}, 
                                                    default_flow_style=False, default_style='|')
        reflection_instruction = f"{system_message}\n{prompt_to_reflect_and_improve(original_instructions, reply_without_improvements)}"
        reply = query_llm(f"{system_message}\n{reflection_instruction}")
        if reply == "No improvements need to be made.":
            log.info("No improvements need to be made.")
            break
        parsed_reply = yaml.safe_load(reply)
        log.info(f"Needed improvements:\n{parsed_reply['improvements']}")
        improvement_iters += 1

    return parsed_reply["path_and_filename"], parsed_reply["file_contents"]
