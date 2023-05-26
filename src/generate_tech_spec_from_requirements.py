"""Generate a technical specification document from the project requirements."""


from pathlib import Path

import fire

from prompt_templates.tech_spec_generation import tech_spec_document_template
from utils.llm import send_templated_message_to_llm
from utils.file_io import read_file, write_file
from config import project_configs


def generate_tech_spec(
    project_name: str,
    max_improvement_iterations_per_llm_query: int = 3
) -> None:
    """Generate a technical specification document from the project requirements.
    
    Args:
        project_path: The path to the project.
        max_improvement_iterations_per_llm_query: 
            The maximum number of improvement iterations per LLM query.
    """
    project_requirements = read_file(Path(project_configs[project_name]["requirements_document"]))
    message_to_send = tech_spec_document_template(
        project_requirements, project_configs[project_name]["project_path"])
    file_content = send_templated_message_to_llm(
        message_to_send, max_improvement_iterations_per_llm_query)
    write_file(
        Path(project_configs[project_name]["project_path"]) / Path("technical_specification.md"),
        file_content)


if __name__ == "__main__":
    fire.Fire(generate_tech_spec)
