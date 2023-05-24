"""Functions for interacting with the OpenAI Language Model (LLM)."""


import os
import yaml

import openai

from prompt_templates.system_message import system_message_template
from utils.log import log


promt_to_respond_with_yaml = """
Your return should be formatted as a valid yaml file:
path_and_filename: <path_and_filename>
file_contents: <file contents>
"""


def query_llm(message: str, max_attempts: int = 3) -> str | None:
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
    while attempts < max_attempts:
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
            log.warning(f"OpenAI rate limit error (attempt {attempts} of {max_attempts})")
            reply = None
        attempts += 1
    return reply


def send_templated_message_to_llm(message: str) -> tuple[str, str]:
    # Anicdotally, sending the system message as the system message (as opposed to just
    # including it in the user message) seems to work better.
    system_message = system_message_template()
    reply = query_llm(
        f"{system_message}\n\n{message}\n\n{promt_to_respond_with_yaml}")
    reply = yaml.safe_load(reply)
    return reply["path_and_filename"], reply["file_contents"]
