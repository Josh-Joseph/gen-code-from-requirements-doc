"""Run the code with self-healing."""


import subprocess
import time
from pathlib import Path

import fire

from prompt_templates.information_retrieval import find_file_with_erorr_template
from prompt_templates.code_generation import fix_code_template
from utils.llm import send_templated_message_to_llm, query_llm
from utils.file_io import read_file, write_file, compute_diffs, get_main_script_name
from utils.log import log
from config import project_configs


def run_script_inside_subprocess_with_timeout(
    root_folder_name: str,
    bash_script: str,
    timeout: str | None = None
) -> tuple[str | None, str | None]:
    """Run the script inside a subprocess with a timeout."""
    start = time.time()
    process = subprocess.Popen([f"./{bash_script}"],
                               cwd=root_folder_name,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    while True:
        if process.poll() is not None:  # If the process has finished
            break
        if timeout is not None:
            if time.time() - start > timeout:  # If timeout has passed
                process.terminate()
                log.debug(f"Script was terminated after {timeout} seconds.")
                return None, None
        time.sleep(0.1)  # Sleep for a short time to prevent busy waiting

    stdout, stderr = process.communicate()

    return stdout, stderr


def run_with_self_healing_code(
    project_name: str,
    max_heal_attempts: int = 25,
    max_improvement_iterations_per_llm_query: int = 3
) -> None:
    """Run the code with self-healing.
    
    Args:
        project_path: The path to the project.
        max_fix_attempts: The maximum number of attempts to fix the code.
        max_improvement_iterations_per_llm_query: 
            The maximum number of improvement iterations per LLM query.
    """
    project_requirements = read_file(Path(project_configs[project_name]["requirements_document"]))
    tech_spec = read_file(
        Path(project_configs[project_name]["project_path"]) / Path("technical_specification.md"))
    root_folder_name = project_configs[project_name]["project_path"]
    bash_script = get_main_script_name(root_folder_name)
    subprocess.run(["chmod", "+x", str(Path(root_folder_name) / Path(bash_script))])
    code_errors_out = True
    attempts = 1
    while code_errors_out and attempts <= max_heal_attempts:
        stdout, stderr = run_script_inside_subprocess_with_timeout(
            root_folder_name, bash_script)

        if stderr is None:
            code_errors_out = False
            log.debug("Script ran successfully.")
        else:
            log.debug(f"Output from stdout: {stdout}")
            log.debug(f"Output from stderr: {stderr}")
            message_to_send = find_file_with_erorr_template(tech_spec, stdout, stderr)
            path_and_file_name = query_llm(message_to_send)
            code = read_file(path_and_file_name)
            message_to_send = fix_code_template(
                project_requirements, tech_spec, path_and_file_name, code, stderr)
            content = send_templated_message_to_llm(
                message_to_send, max_improvement_iterations_per_llm_query)
            log.info(compute_diffs(code, content))
            write_file(path_and_file_name, content)
            attempts += 1


if __name__ == "__main__":
    fire.Fire(run_with_self_healing_code)
