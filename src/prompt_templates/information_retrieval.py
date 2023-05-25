def find_project_root_directory_name_template(design):
    return f"""Given on the following design document:
```markdown
{design}
```

What is the name of the project root directory?
Only respond with the name of the root directory, not the full path.
Do not include any other text or formatting."""


def find_project_main_script_name_template(design):
    return f"""Given on the following design document:
```markdown
{design}
```

What is the path and filename of the bash script that runs the code?
Only respond with the path and filename to the bash script from the project's root directory.
Do not include any other text or formatting.
Only respond with the single string."""


def find_project_files_to_generate_template(design):
    return f"""Given on the following design document:
```markdown
{design}
```

What is the path and filenames of all the files listed in the design document as part of the codebase?
Do not include any other text or formatting.
Only respond with a Python-style list containing these files."""


def find_file_with_erorr_template(design, stdout, stderr):
    return f"""Given on the following design document:
```markdown
{design}
```

When the codebase is run, this is stdout:
{stdout}

When the codebase is run, this is stderr:
{stderr}

What file is causing the script to not as desired?
Only respond with the filename (including its path).
Do not include any other text or formatting."""


def find_code_improvements_template(requirements, design, filename, code):
    return f"""These are the requirements for the codebase:
```markdown
{requirements}
```

And the design document:
```markdown
{design}
```

The code for {filename} is:
```
{code}
```

Your instructions are to only respond with either:
- A bullet point list of the improvements that should be made to the code for {filename}.
- The string 'No improvements need to be made.'

Under no circumstances should you suggest a change or improvement that conflicts with what is written in the requirements document or design document."""