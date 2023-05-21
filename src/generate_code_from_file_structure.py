"""Generate the file structure from the design document."""


from pathlib import Path

import fire

from prompt_templates.code_generation import code_template
from prompt_templates.information_retrieval import project_root_directory_name_template
from utils.llm import send_templated_message_to_llm, query_llm
from utils.file_io import load_design_document, write_file


def get_file_paths(directory):
    file_paths = []
    for filepath in Path(directory).rglob('*'):
        if filepath.is_file():
            file_paths.append(str(filepath))
    return file_paths


def get_project_root_folder_name(project_path: str) -> str:
    """Get the project root folder name by looking it up in the design document.
    
    Args:
        project_path: The path to the project.
    
    Returns:
        The project root folder name.
    """
    design_document = load_design_document(project_path)
    message_to_send = project_root_directory_name_template(design_document)
    reply = query_llm(message_to_send)
    return reply


def generate_code(project_path: str) -> None:
    """Generate the file structure from the design document.
    
    Args:
        project_path: The path to the project.
    """
    design_document = load_design_document(project_path)
    root_folder_name = get_project_root_folder_name(project_path)
    file_paths = get_file_paths(f"{project_path}/{root_folder_name}")
    for fp in file_paths:
        message_to_send = code_template(design_document, fp)
        path_and_filename, content = send_templated_message_to_llm(message_to_send)
        write_file(path_and_filename, content)


if __name__ == "__main__":
    fire.Fire(generate_code)
