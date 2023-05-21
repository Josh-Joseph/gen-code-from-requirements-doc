"""Generate the file structure from the design document."""


import logging

from prompt_templates.code_generation import file_structure_template
from utils.llm import send_templated_message_to_llm
from utils.file_io import load_design_document, write_file


logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s | %(levelname)s | %(message)s",
                    datefmt='%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
    project_path = "generated_projects/discord_bot"
    design_document = load_design_document(project_path)
    message_to_send = file_structure_template(design_document, project_path)
    path_and_filename, content = send_templated_message_to_llm(message_to_send)
    write_file(path_and_filename, content)
