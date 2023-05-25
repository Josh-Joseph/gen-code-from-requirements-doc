"""Generate a design document from the project requirements."""


import fire

from prompt_templates.design_doc_generation import design_document_template
from utils.llm import send_templated_message_to_llm
from utils.file_io import load_project_requirements, write_file
from config import project_configs


def generate_design_doc(project_name: str) -> None:
    """Generate a design document from the project requirements.
    
    Args:
        project_path: The path to the project.
    """
    project_requirements = load_project_requirements(project_configs[project_name]["requirements_document"])
    message_to_send = design_document_template(project_requirements, project_configs[project_name]["project_path"])
    path_and_filename, content = send_templated_message_to_llm(message_to_send, max_improvement_iterations=3)
    write_file(path_and_filename, content)


if __name__ == "__main__":
    fire.Fire(generate_design_doc)
