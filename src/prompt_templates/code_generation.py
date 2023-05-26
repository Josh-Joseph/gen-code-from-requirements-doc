def code_template(requirements, tech_spec, file_path):
    return f"""This is the requirements document for the codebase:
```markdown
{requirements}
```
     
And the corresponding technical specification document:
```markdown
{tech_spec}
```

Your instructions:
- Generate the content for {file_path} only. Look at the file extension to know what type of content to generate.
- Only respond with the filename (including the full path you were given) and contents for the single file.
- Do not write any re-amble or post-amble text around the single file.
- If you are generating code, all code must be cleanly-written, full, valid, correct, and runnable.
- All code must be consistent with the requirements document and technical specification document."""


def bash_script_template(tech_spec):
    return f"""Given on the following technical specification document:
```markdown
{tech_spec}
```

Your instructions:
- Generate the a bash script to set up the virtual environment, install the dependencies, and run the code. Assume the bash script will be run from the project's root directory.
- Ensure the bash script is correct and only uses valid bash syntax.
- Do not write any re-amble or post-amble text around the single file.
- If you are generating code, all code must be cleanly-written, full, valid, correct, and runnable."""


def fix_code_template(requirements, tech_spec, filename, code, stderr):
    return f"""This is the requirements document for the codebase:
```markdown
{requirements}
```
     
And the corresponding technical specification document:
```markdown
{tech_spec}
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
