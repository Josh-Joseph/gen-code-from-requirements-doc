"""Generate the file structure from the design document."""


import fire


from prompt_templates.code_generation import file_structure_template
from utils.llm import send_templated_message_to_llm
from utils.file_io import load_design_document, write_file


def generate_file_structure(project_path: str) -> None:
    """Generate the file structure from the design document.
    
    Args:
        project_path: The path to the project.
    """
    design_document = load_design_document(project_path)
    message_to_send = file_structure_template(design_document, project_path)
    path_and_filename, content = send_templated_message_to_llm(message_to_send)
    write_file(path_and_filename, content)


if __name__ == "__main__":
    fire.Fire(generate_file_structure)
