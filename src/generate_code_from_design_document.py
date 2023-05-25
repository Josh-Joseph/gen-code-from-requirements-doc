"""Generate the file structure from the design document."""


import time


import fire
from joblib import Parallel, delayed

from prompt_templates.information_retrieval import find_project_files_to_generate_template
from prompt_templates.code_generation import code_template
from utils.llm import send_templated_message_to_llm
from utils.file_io import load_project_requirements, load_design_document, write_file, get_file_paths, get_files_to_generate
from config import project_configs


def generate_code(project_name: str, n_jobs: int | None = None) -> None:
    """Generate the file structure from the design document.

    Args:
        project_path: The path to the project.
        n_jobs: The number of jobs to run in parallel. If None, then the number of 
            jobs is set to the number of files. Note it's more common to set it to 
            the number of cores on your machine but since the majority of the time
            is spent waiting for a response from LLM, it's better. At some
            number of number of files >> number of cores this will break.
    """
    project_requirements = load_project_requirements(project_configs[project_name]["requirements_document"])
    design_document = load_design_document(project_configs[project_name]["project_path"])
    root_folder_name = project_configs[project_name]["project_path"]
    files_to_generate = get_files_to_generate(design_document)
    file_paths = [f"{root_folder_name}/{file_to_generate}" for file_to_generate in files_to_generate]

    def process_file(fp, wait_seconds):
        time.sleep(wait_seconds)  # Wait to prevent overloading LLM API
        message_to_send = code_template(project_requirements, design_document, fp)
        path_and_filename, content = send_templated_message_to_llm(message_to_send, max_improvement_iterations=3)
        write_file(path_and_filename, content)

    if n_jobs is None:
        n_jobs = len(file_paths)
    print("*************************fix njobs!!!")
    # Parallel(n_jobs=n_jobs)(delayed(process_file)(fp, wait_seconds) 
    Parallel(n_jobs=1)(delayed(process_file)(fp, wait_seconds) 
                                     for wait_seconds, fp in enumerate(file_paths))

if __name__ == "__main__":
    fire.Fire(generate_code)
