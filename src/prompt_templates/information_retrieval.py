def find_project_root_directory_name_template(design):
    return f"""Given on the following design document:
```markdown
{design}
```

What is the name of the project root directory?
Only respond with the name of the root directory, not the full path.
Do not include any other text or formatting."""


def find_file_with_erorr_template(design, stderr):
    return f"""Given on the following design document:
```markdown
{design}
```

When the codebase is run, the following error is thrown:
{stderr}

What file is causing the error?
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

All suggestions must be consistent with the requirements document and design document."""