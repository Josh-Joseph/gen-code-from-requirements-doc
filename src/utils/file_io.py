"""File IO utilities for the project."""


from pathlib import Path
import difflib


from prompt_templates.information_retrieval import (find_project_root_directory_name_template,
                                                    find_project_main_script_name_template)
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


def get_main_script_name(project_path: str) -> str:
    """Get the main script name by looking it up in the design document.

    Args:
        project_path: The path to the project.

    Returns:
        The main script name.
    """
    design_document = load_design_document(project_path)
    message_to_send = find_project_main_script_name_template(design_document)
    reply = query_llm(message_to_send)
    return reply


def load_code_file(project_path: str, root_folder_name: str, file_path: str) -> str:
    """Load the code file from the project."""
    with open(f"{project_path}/{root_folder_name}/{file_path}", "r") as file:
        code = file.read()
    return code


def compute_diffs(original: str, modified: str) -> str:
    """Compute the diffs between the original and modified code."""
    diff = difflib.unified_diff(
        original.splitlines(),
        modified.splitlines(),
        lineterm='',
        fromfile='Original',
        tofile='Modified')
    return '\n'.join(diff)


def get_file_paths(directory: str) -> list[str]:
    file_paths = []
    for filepath in Path(directory).rglob('*'):
        if filepath.is_file():
            file_paths.append(str(filepath))
    return file_paths
