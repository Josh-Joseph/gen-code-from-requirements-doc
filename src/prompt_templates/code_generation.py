def code_template(requirements, design, file_path):
    return f"""This is the requirements document for the codebase:
```markdown
{requirements}
```
     
And the design document:
```markdown
{design}
```

Your instructions:
- Generate the content for {file_path} only. Look at the file extension to know what type of content to generate.
- Only respond with the filename (including the full path you were given) and contents for the single file.
- Do not write any re-amble or post-amble text around the single file.
- If you are generating code, all code must be cleanly-written, full, valid, correct, and runnable.
- All code must be consistent with the requirements document and design document."""


def file_structure_template(design, project_path):
    return f"""Write a Python script which generates file structure based on the following design document:
```markdown
{design}
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
    return f"""Given on the following design document:
```markdown
{design}
```

Your instructions:
- Generate the a bash script to set up the virtual environment, install the dependencies, and run the code. Assume the bash script will be run from the project's root directory.
- Ensure the bash script is correct and only uses valid bash syntax.
- Do not write any re-amble or post-amble text around the single file.
- If you are generating code, all code must be cleanly-written, full, valid, correct, and runnable."""


def fix_code_template(requirements, design, filename, code, stderr):
    return f"""This is the requirements document for the codebase:
```markdown
{requirements}
```
     
And the design document:
```markdown
{design}
```

When the code for {filename} is run:
```
{code}
```

It throws the following error:
```
{stderr}
```

Your instructions:
- Generate the content for {filename} only. Look at the file extension to know what type of content to generate.
- Do not write any re-amble or post-amble text around the single file.
- If you are generating code, all code must be cleanly-written, full, valid, correct, and runnable.
- Make sure the updated code you respond with fixes the error that was thrown from the original code.
- Look carefully through the code and fix any additional errors you find or improvements that should be made."""


def improve_code_template(requirements, design, filename, code, improvements):
    return f"""These are the requirements for the codebase:
```markdown
{requirements}
```
     
And the design document:
```markdown
{design}
```

And here is the code for {filename}:
```
{code}
```

Here are the necessary improvements:
{improvements}

Your instructions:
- Generate the content for {filename} only. Look at the file extension to know what type of content to generate.
- Do not write any re-amble or post-amble text around the single file.
- If you are generating code, all code must be cleanly-written, full, valid, correct, and runnable.
- Make sure the updated code you respond with includes the necessary improvements.
- Look carefully through the code and fix any additional errors you find or improvements that should be made.
- Under no circumstances should you make a change that conflicts with what is written in the requirements document or design document."""
