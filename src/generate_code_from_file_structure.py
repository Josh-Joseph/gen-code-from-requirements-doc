"""Generate the file structure from the design document."""


import time


import fire
from joblib import Parallel, delayed

from prompt_templates.code_generation import code_template
from utils.llm import send_templated_message_to_llm
from utils.file_io import (load_project_requirements, load_design_document, 
                           get_project_root_folder_name, write_file, get_file_paths)


def generate_code(project_path: str, n_jobs: int | None = None) -> None:
    """Generate the file structure from the design document.

    Args:
        project_path: The path to the project.
        n_jobs: The number of jobs to run in parallel. If None, then the number of 
            jobs is set to the number of files. Note it's more common to set it to 
            the number of cores on your machine but since the majority of the time
            is spent waiting for a response from LLM, it's better. At some
            number of number of files >> number of cores this will break.
    """
    project_requirements = load_project_requirements(project_path)
    design_document = load_design_document(project_path)
    root_folder_name = get_project_root_folder_name(project_path)
    file_paths = get_file_paths(f"{project_path}/{root_folder_name}")

    def process_file(fp, wait_seconds):
        time.sleep(wait_seconds)  # Wait to prevent overloading LLM API
        message_to_send = code_template(project_requirements, design_document, fp)
        path_and_filename, content = send_templated_message_to_llm(message_to_send)
        write_file(path_and_filename, content)

    Parallel(n_jobs=len(file_paths))(delayed(process_file)(fp, wait_seconds) 
                                     for wait_seconds, fp in enumerate(file_paths))

if __name__ == "__main__":
    fire.Fire(generate_code)
