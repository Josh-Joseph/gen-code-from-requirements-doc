import os
import yaml
import logging

import openai

from prompt_templates.system_message import system_message_template


promt_to_respond_with_yaml = """
Your return should be formatted as a valid yaml file:
path_and_filename: <path_and_filename>
file_contents: <file contents>
"""


def query_llm(message: str) -> str:
    """Send the system message and design message to OpenAI and return the reply."""
    openai.api_key = os.getenv("OPENAI_KEY")

    openai_model = "gpt-4"
    openai_model_max_tokens = 2048

    logging.debug(f"llm query:\n{message}")
    messages = []
    messages.append({"role": "user", "content": message})

    params = {
        "model": openai_model,
        "messages": messages,
        "max_tokens": openai_model_max_tokens,
        "temperature": 0,
    }
    response = openai.ChatCompletion.create(**params)
    reply = response.choices[0]["message"]["content"]
    logging.debug(f"llm reply:\n{reply}")
    return reply


def send_templated_message_to_llm(message: str) -> tuple[str, str]:
    # Anicdotally, sending the system message as the system message (as opposed to just
    # including it in the user message) seems to work better.
    system_message = system_message_template()
    reply = query_llm(f"{system_message}\n\n{message}\n\n{promt_to_respond_with_yaml}")
    reply = yaml.safe_load(reply)
    return reply["path_and_filename"], reply["file_contents"]
