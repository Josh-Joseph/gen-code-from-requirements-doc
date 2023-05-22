"""Fix the code for the project."""


from pathlib import Path
import subprocess
import difflib
import time

import fire

from prompt_templates.information_retrieval import find_file_with_erorr_template
from prompt_templates.code_generation import fix_code_template
from utils.llm import send_templated_message_to_llm, query_llm
from utils.file_io import load_project_requirements, load_design_document, get_project_root_folder_name, write_file, load_code_file
from utils.log import log


def compute_diffs(original: str, modified: str) -> str:
    """Compute the diffs between the original and modified code."""
    diff = difflib.unified_diff(
        original.splitlines(),
        modified.splitlines(),
        lineterm='',
        fromfile='Original',
        tofile='Modified')
    return '\n'.join(diff)


def run_script_inside_subprocess_with_timeout(
    project_path: str,
    root_folder_name: str,
    bash_script: str,
    timeout: str = 10
) -> tuple[str | None, str | None]:
    """Run the script inside a subprocess with a timeout."""
    start = time.time()
    process = subprocess.Popen([f"./{bash_script}"], cwd=f"{project_path}/{root_folder_name}",
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        if process.poll() is not None:  # If the process has finished
            break
        if time.time() - start > timeout:  # If timeout has passed
            process.terminate()
            log.debug(f"Script was terminated after {timeout} seconds.")
            return None, None
        time.sleep(0.1)  # Sleep for a short time to prevent busy waiting

    stdout, stderr = process.communicate()

    return stdout, stderr


def fix_code(project_path: str, bash_script: str, max_attempts: int = 5) -> None:
    """Fix the code for the project.
    
    Args:
        project_path: The path to the project.
        bash_script: The name of the bash script to run.
        max_attempts: The maximum number of attempts to fix the code.
    """
    project_requirements = load_project_requirements(project_path)
    design_document = load_design_document(project_path)
    root_folder_name = get_project_root_folder_name(project_path)
    code_errors_out = True
    attemps = 1
    while code_errors_out and attemps <= max_attempts:
        stdout, stderr = run_script_inside_subprocess_with_timeout(
            project_path, root_folder_name, bash_script)

        if stderr is None:
            code_errors_out = False
            log.debug("Script ran successfully.")
        else:
            log.debug(f"stdout: {stdout}")
            log.debug(f"stderr: {stderr}")
            message_to_send = find_file_with_erorr_template(
                design_document, stderr)
            reply = query_llm(message_to_send)
            code = load_code_file(project_path, root_folder_name, reply)
            message_to_send = fix_code_template(
                project_requirements, design_document, reply, code, stderr)
            path_and_filename, content = send_templated_message_to_llm(
                message_to_send)
            log.info(compute_diffs(code, content))
            write_file(
                f"{project_path}/{root_folder_name}/{path_and_filename}", content)
            attemps += 1


if __name__ == "__main__":
    fire.Fire(fix_code)
