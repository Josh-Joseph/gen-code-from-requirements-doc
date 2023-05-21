"""Generate the file structure from the design document."""


import logging
from pathlib import Path

from prompt_templates.code_generation import code_template
from utils.llm import send_templated_message_to_llm
from utils.file_io import load_design_document, write_file


logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s | %(levelname)s | %(message)s",
                    datefmt='%Y-%m-%d %H:%M:%S')


def get_file_paths(directory):
    file_paths = []
    for filepath in Path(directory).rglob('*'):
        if filepath.is_file():
            file_paths.append(str(filepath))
    return file_paths


if __name__ == "__main__":
    project_path = "generated_projects/discord_bot"
    design_document = load_design_document(project_path)
    file_paths = get_file_paths(f"{project_path}/discord_character_counter")
    for fp in file_paths:
        message_to_send = code_template(design_document, fp)
        path_and_filename, content = send_templated_message_to_llm(message_to_send)
        write_file(path_and_filename, content)
