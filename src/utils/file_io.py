"""File IO utilities for the project."""


from prompt_templates.information_retrieval import find_project_root_directory_name_template
from utils.llm import query_llm
from utils.log import log


def load_project_requirements(project_path: str) -> str:
    """Load the project requirements from the project_requirements_document.md file."""
    with open(f"{project_path}/project_requirements_document.md", "r") as file:
        project_requirements = file.read()
    return project_requirements


def load_design_document(project_path: str) -> str:
    """Load the project design document from the project_design_document.md file."""
    with open(f"{project_path}/project_design_document.md", "r") as file:
        design_document = file.read()
    return design_document


def write_file(path_and_filename: str, content: str) -> None:
    """Write the content to the file."""
    with open(path_and_filename, "w") as file:
        file.write(content)
    log.info(f"Wrote out file: {path_and_filename}")


def get_project_root_folder_name(project_path: str) -> str:
    """Get the project root folder name by looking it up in the design document.
    
    Args:
        project_path: The path to the project.
    
    Returns:
        The project root folder name.
    """
    design_document = load_design_document(project_path)
    message_to_send = find_project_root_directory_name_template(design_document)
    reply = query_llm(message_to_send)
    return reply


def load_code_file(project_path: str, root_folder_name: str, file_path: str) -> str:
    """Load the code file from the project."""
    with open(f"{project_path}/{root_folder_name}/{file_path}", "r") as file:
        code = file.read()
    return code
