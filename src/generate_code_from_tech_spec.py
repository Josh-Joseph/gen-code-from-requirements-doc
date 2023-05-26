"""Generate the file structure from the technical specification document."""


from pathlib import Path
import time

import fire
from joblib import Parallel, delayed

from prompt_templates.code_generation import code_template
from utils.llm import send_templated_message_to_llm
from utils.file_io import read_file, write_file, get_files_to_generate
from config import project_configs


def process_file(
    fp: str,
    project_requirements: str,
    tech_spec: str,
    wait_seconds: int,
    max_improvement_iterations: int
) -> None:
    """Process a file."""
    if "technical_specification.md" in fp:  # don't overwrite this file
        return
    time.sleep(wait_seconds)  # Wait to prevent overloading LLM API
    message_to_send = code_template(project_requirements, tech_spec, fp)
    content = send_templated_message_to_llm(
        message_to_send, max_improvement_iterations=max_improvement_iterations)
    write_file(fp, content)


def generate_code(
    project_name: str,
    max_improvement_iterations_per_llm_query: int = 3,
    n_jobs: int | None = 1
) -> None:
    """Generate the code for a technical specification.

    Args:
        project_path: The path to the project.
        max_improvement_iterations_per_llm_query: 
            The maximum number of improvement iterations per LLM query.
        n_jobs: The number of jobs to run in parallel. If None, then the number of 
            jobs is set to the number of files. Note it's more common to set it to 
            the number of cores on your machine but since the majority of the time
            is spent waiting for a response from LLM, it's better. At some
            number of number of files > number of cores this will break.
    """
    project_requirements = read_file(
        Path(project_configs[project_name]["requirements_document"]))
    tech_spec = read_file(
        Path(project_configs[project_name]["project_path"]) / Path("technical_specification.md"))
    files_to_generate = get_files_to_generate(tech_spec)

    if n_jobs is None:
        n_jobs = len(files_to_generate)
    Parallel(n_jobs=n_jobs)(delayed(process_file)(
        fp, project_requirements,
        tech_spec,
        5 * wait_seconds,
        max_improvement_iterations_per_llm_query)
        for wait_seconds, fp in enumerate(files_to_generate))
    # for wait_seconds, fp in enumerate(files_to_generate):
    # process_file(fp, project_requirements, tech_spec, wait_seconds,
    #              max_improvement_iterations=max_improvement_iterations_per_llm_query)


if __name__ == "__main__":
    fire.Fire(generate_code)
