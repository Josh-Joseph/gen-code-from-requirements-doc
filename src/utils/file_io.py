"""File IO utilities for the project."""


from pathlib import Path
import difflib


from prompt_templates.information_retrieval import (
    find_project_root_directory_name_template, find_project_main_script_name_template, 
    find_project_files_to_generate_template)
from utils.llm import query_llm
from utils.log import log


def read_file(path_and_filename: str) -> str:
    """Read the file from the path_and_filename."""
    with open(path_and_filename, "r") as file:
        file_contents = file.read()
    return file_contents


def write_file(path_and_filename: str, content: str) -> None:
    """Write the content to the file."""
    Path(path_and_filename).parent.mkdir(parents=True, exist_ok=True)
    with open(path_and_filename, "w") as file:
        file.write(content)
    log.debug(f"Wrote out file: {path_and_filename}")


def get_project_root_folder_name(project_path: str) -> str:
    """Get the project root folder name by looking it up in the technical specification document.
    
    Args:
        project_path: The path to the project.
    
    Returns:
        The project root folder name.
    """
    tech_spec = read_file(Path(project_path) / Path("technical_specification.md"))
    message_to_send = find_project_root_directory_name_template(tech_spec)
    reply = query_llm(message_to_send)
    return reply


def get_main_script_name(project_path: str) -> str:
    """Get the main script name by looking it up in the technical specification document.

    Args:
        project_path: The path to the project.

    Returns:
        The main script name.
    """
    tech_spec = read_file(Path(project_path) / Path("technical_specification.md"))
    message_to_send = find_project_main_script_name_template(tech_spec)
    reply = query_llm(message_to_send)
    return reply


def get_files_to_generate(tech_spec: str) -> list[str]:
    message_to_send = find_project_files_to_generate_template(tech_spec)
    reply = query_llm(message_to_send)
    return eval(reply)


def load_code_file(root_folder_name: str, file_path: str) -> str:
    """Load the code file from the project."""
    with open(f"{root_folder_name}/{file_path}", "r") as file:
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
