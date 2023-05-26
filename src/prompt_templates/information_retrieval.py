def find_project_root_directory_name_template(tech_spec):
    return f"""Given the following technical specification document:
```markdown
{tech_spec}
```

What is the name of the project root directory?
Only respond with the name of the root directory, not the full path.
Do not include any other text or formatting."""


def find_project_main_script_name_template(tech_spec):
    return f"""Given the following technical specification document:
```markdown
{tech_spec}
```

What is the filename of the bash script that runs the code?
Only respond with the filename to the bash script from the project's root directory.
Do not include any other text or formatting.
Only respond with the single string."""


def find_project_files_to_generate_template(tech_spec):
    return f"""Given the following technical specification document:
```markdown
{tech_spec}
```

What are the filenames of all the files listed in the technical specification document as part of the codebase (include the full path to the file from the project's root directory)?
Do not include any other text or formatting.
Only respond with a Python-style list containing these files."""


def find_file_with_erorr_template(tech_spec, stdout, stderr):
    return f"""Given the following technical specification document:
```markdown
{tech_spec}
```

When the codebase is run, this is stdout:
{stdout}

When the codebase is run, this is stderr:
{stderr}

What file should be edited in order to fix the error?
Only respond with the path (including the codebases's root folder) and filename.
Do not include any other text or formatting."""
