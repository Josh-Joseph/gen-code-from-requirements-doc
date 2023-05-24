"""Improve the code for the project."""


from pathlib import Path
import subprocess
import time

import fire
from joblib import Parallel, delayed

from prompt_templates.information_retrieval import find_code_improvements_template
from prompt_templates.code_generation import improve_code_template
from utils.llm import send_templated_message_to_llm, query_llm
from utils.file_io import (load_project_requirements, load_design_document, get_project_root_folder_name,
                           write_file, load_code_file, get_file_paths, compute_diffs)
from utils.log import log


def improve_code(project_path: str, max_attempts: int = 3) -> None:
    """Improve the code for the project.

    Args:
        project_path: The path to the project.
        max_attempts: The maximum number of attempts to fix the code.
    """
    project_requirements = load_project_requirements(project_path)
    design_document = load_design_document(project_path)
    root_folder_name = get_project_root_folder_name(project_path)
    file_paths = get_file_paths(f"{project_path}/{root_folder_name}")
    
    def process_file(fp, wait_seconds):
        time.sleep(wait_seconds)  # Wait to prevent overloading LLM API
        attempts = 1
        needs_improvement = True
        while needs_improvement and attempts <= max_attempts:
            file_path = fp.replace(f"{project_path}/{root_folder_name}/", "")
            code = load_code_file(project_path, root_folder_name, file_path)
            message_to_send = find_code_improvements_template(project_requirements, design_document, file_path, code)
            reply = query_llm(message_to_send)

            if reply == "No improvements need to be made.":
                log.debug(f"No improvements need to be made for {fp}.")
                needs_improvement = False
            else:
                log.info(f"The following improvements were suggested: {reply}")
                message_to_send = improve_code_template(project_requirements, design_document, file_path, code, reply)
                path_and_filename, content = send_templated_message_to_llm(
                    message_to_send)
                log.info(compute_diffs(code, content))
                write_file(
                    f"{project_path}/{root_folder_name}/{path_and_filename}", content)
                attempts += 1

    Parallel(n_jobs=len(file_paths))(delayed(process_file)(fp, wait_seconds) 
                                     for wait_seconds, fp in enumerate(file_paths))


if __name__ == "__main__":
    fire.Fire(improve_code)
