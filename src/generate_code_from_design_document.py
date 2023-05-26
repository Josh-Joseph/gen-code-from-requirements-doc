"""Generate the file structure from the design document."""


from pathlib import Path
import time

import fire
from joblib import Parallel, delayed

from prompt_templates.code_generation import code_template
from utils.llm import send_templated_message_to_llm
from utils.file_io import read_file, write_file, get_files_to_generate
from config import project_configs


def process_file(fp, project_requirements, design_document, wait_seconds):
    if "project_design_document.md" in fp:
        return
    time.sleep(wait_seconds)  # Wait to prevent overloading LLM API
    message_to_send = code_template(project_requirements, design_document, fp)
    content = send_templated_message_to_llm(message_to_send, max_improvement_iterations=3)
    write_file(fp, content)


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
    project_requirements = read_file(Path(project_configs[project_name]["requirements_document"]))
    design_document = read_file(
        Path(project_configs[project_name]["project_path"]) / Path("project_design_document.md"))
    root_folder_name = project_configs[project_name]["project_path"]
    files_to_generate = get_files_to_generate(design_document)

    if n_jobs is None:
        n_jobs = len(files_to_generate)
    # Parallel(n_jobs=n_jobs)(delayed(process_file)(
    #     fp, project_requirements, design_document, wait_seconds) 
    #     for wait_seconds, fp in enumerate(file_paths))
    for wait_seconds, fp in enumerate(files_to_generate):
        process_file(fp, project_requirements, design_document, wait_seconds)


if __name__ == "__main__":
    fire.Fire(generate_code)
