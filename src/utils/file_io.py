def load_project_requirements(project_path: str) -> str:
    """Load the project requirements from the project_requirements_document.md file."""
    with open(f"{project_path}/project_requirements_document.md", "r") as file:
        project_requirements = file.read()
    return project_requirements


def load_design_document(project_path: str) -> str:
    """Load the project design document from the project_design_document.md file."""
    with open(f"{project_path}/project_design_document.md", "r") as file:
        design_document = file.read()
    return design_document


def write_file(path_and_filename: str, content: str) -> None:
    """Write the content to the file."""
    with open(path_and_filename, "w") as file:
        file.write(content)
