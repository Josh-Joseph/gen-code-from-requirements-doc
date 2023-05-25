def design_document_template(project_requirements, file_path):
    return f"""These are the requirements for the codebase:
```markdown
{project_requirements}
```

Write a design document based on these requirements. The design document must:
- Be written as a markdown file named `{file_path}/project_design_document.md`.
- Have the following sections:
    - A table of contents
    - Last updated date
    - An overview of the project. This should contain a description of the purpose of the project.
    - Setup and usage instructions.
    - Dependency diagram. A diagram drawn written in graphviz syntax that shows the dependencies between the different modules, directories, and files of the project.
        - Include any third-party libraries that will be used in the diagram.
    - A tree diagram of the modules, directories and file structure as it would look if we were to created by running `tree -a` on a linux system. Order the modules, directories, and files as they would be by `tree` on a linux file system. Alphabetized with folders and files starting with a `.` at the top.
        - Include the project root directory {file_path} in the tree diagram.
        - Include a `src` and `tests` directory. Each python file in the `src` directory must have a test file in `tests` directory.
        - Do not make `src` a module (i.e., don't include `__init__.py` file in the `src` directory).
        - Include any additional files that are necessary for the project to be built and run. Optional examples of these are: a setup.py file, a Dockerfile, a Makefile, a .gitignore file, github actions workflow `.yaml` files, etc.
        - Include a `readme.md` file, a `requirements.txt` file, and a LICENSE file.
        - Include a `project_design_document.md` file.
        - Do not include `.env` files, a `.gitignore` file, a `.git` directory, or a `.venv` directory.
    - Logging. This section must include what logging will be used throughout the codebase.
    - For each file (not folder) in the file structure with the sections ordered by Python files first, then the other files:
        - Create a section for each file. Only create sections for files. Do not create sections for directories.
        - Write a description of what the purpose of the file is as the first lines of this section. Do not make this description a bullet point.
        - List any third-party Python packages that will be used in the file.
        - List of any environment variables the file will use.
        - Populate the section with each function, class, and class method that will appear in the file and bullets. Do not create subsections for each function, class, and class method. Include a description for each function, class, and class method as sub-bullets. Include an example input-output pair for each function and class method, when applicable as sub-bullets.
        - Include the full function, method, and class initialization signatures with type hints and docstrings.
        - An example section should look like:
            ```markdown
            <filename>
            <purpose of the file>
            - <fuction and class content>
            - ...
            ```

Only create the design markdown document. Do not generate any of the specific code files."""
