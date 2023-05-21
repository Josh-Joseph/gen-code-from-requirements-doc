def code_template(design, file_path):
    return f"""Given on the following design:
{design}

Your Instructions:
- Generate the content for {file_path} only. Look at the file extension to know what type of content to generate.
- Only respond with the filename (including the full path you were given) and contents for the single Python file.
- Do not write any re-amble or post-amble text around the single file.
- If you are generating code, all code must be cleanly-written, full, valid, correct, and runnable."""


def file_structure_template(design_document, project_path):
    return f"""Write a Python script which generates file structure based on the following design document:
```markdown
{design_document}
```

Only respond with a single Python file named `generate_file_structure.py`.
The Python script must:
- Be contained in the `{project_path}` directory.
- Name the project root directory the title of the design document (lowercased with underscores). We'll refer to this as `project_root`.
- Create a function called `create_directory_structure` which takes the path (`{project_path}`) as an argument.
- Check if the `{project_path}/project_root` directory already exists in the function `create_directory_structure`. If it does, delete it and all of its contents.
- Create an empty file for each file that appear in the `File Descriptions` section of the design document.
Do not write any code that will go in the files described in the design document.
Do not write any re-amble or post-amble text around the single Python file.
Respond with full, valid, correct, and runnable Python code."""


def bash_script_template(design):
    return f"""Given on the following design:
{design}

Your instructions:
- Generate the a bash script to set up the virtual environment, install the dependencies, and run the code. Assume the bash script will be run from the project's root directory.
- Ensure the bash script is correct and only uses valid bash syntax.
- Do not write any re-amble or post-amble text around the single file.
- If you are generating code, all code must be cleanly-written, full, valid, correct, and runnable."""
