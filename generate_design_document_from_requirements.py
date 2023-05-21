"""Generate a design document from the project requirements."""


import logging

from prompt_templates.design_doc_generation import design_document_template
from llm_utils import send_templated_message_to_llm
from file_io_utils import load_project_requirements, write_file


logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s | %(levelname)s | %(message)s",
                    datefmt='%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
    project_path = "generated_projects/discord_bot"
    project_requirements = load_project_requirements(project_path)
    message_to_send = design_document_template(project_requirements, project_path)
    path_and_filename, content = send_templated_message_to_llm(message_to_send)
    write_file(path_and_filename, content)
