def project_root_directory_name_template(project_requirements):
    return f"""These are the requirements for the codebase:
```markdown
{project_requirements}
```

What is the name of the project root directory?
Only respond with the name of the root directory, not the full path.
Do not include sany other text or formatting."""