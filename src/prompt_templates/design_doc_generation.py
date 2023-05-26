def design_document_template(project_requirements, file_path):
    return f"""These are the requirements for the codebase:
```markdown
{project_requirements}
```

Write a design document based on these requirements. The design document must:
- Have the following sections:
    - A table of contents
    - Last updated date
    - An overview of the project. This should contain a description of the objective of the project.
    - Setup and usage instructions. Include the codebase's root folder ({file_path}) and make it clear all commands will be run from this location.
    - Code organization. A tree diagram of the codebase as it would look if we were to created by `tree -a` on a linux system. The tree diagram:
        - You must include the following: 
            - a `src` module. Make sure to include a `__init__.py` file so it can be imported by the tests.
            - a `tests` directory with a test file for each Python file in the `src`.
            - `readme.md`
            - `requirements.txt`
            - LICENSE
            - `project_design_document.md`
        - Must not include the following:
            - `.env`
            - `.gitignore`
            - `.git`
            - `.venv`
    - Dependency diagram which must:
        - Be drawn written in graphviz syntax that shows the dependencies between the different modules, directories, and files of the project.
        - Include any third-party Python libraries that will be used in the diagram.
    - Logging. This section must include what logging will be used throughout the codebase.
    - Individual file contents. For each file in the code organization tree:
        - Create a section for each file. Only create sections for files. Do not create sections for directories.
        - Each section must have the following:
            - A description of the purpose of the file as the first lines of this section. Do not make this description a bullet point.
            - The functions, classes, and class methods that must be contained in the file in order to create a functional codebase that achieves the objectives of the project. Format these as bullets inside each section. 
            - An example section should look like:
                ```markdown
                <filename>
                <purpose of the file>
                - <fuction and class content>
                - ...
                ```
            - For each function, class, and class method must include:
                - The full function, method, and class initialization signatures with type hints and a docstring.
                - A description. This must provide sufficient information so that a developer can understand what each file does, how it must be written it, and how it should be used.
                - For test files, you must include at least one test for each function and method for its corresponding Python file in `src`.
                - An example input-output pair for each function and class method, if the function or method takes any arguments.
                - A list of third-party Python packages that will be used in the file, if any are used.
                - A list of environment variables the file will use, if any are used.

Only create the design markdown document. Do not generate any of the specific code files."""
