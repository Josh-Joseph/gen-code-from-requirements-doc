from pathlib import Path


def create_directory_structure(project_path: Path):
    project_root = project_path / "gce_discord_bot"
    if project_root.exists():
        for item in project_root.glob("*"):
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                item.rmdir()
        project_root.rmdir()

    project_root.mkdir()
    (project_root / ".github" / "workflows").mkdir(parents=True)
    (project_root / "src").mkdir()

    files_to_create = [
        ".github/workflows/deploy.yaml",
        "src/discord_bot.py",
        "src/message_handler.py",
        "src/run_bot.py",
        ".gitignore",
        "LICENSE",
        "README.md",
        "requirements.txt",
        "project_design_document.md",
    ]

    for file_path in files_to_create:
        (project_root / file_path).touch()


if __name__ == "__main__":
    project_path = Path("generated_projects/gce_discord_bot")
    create_directory_structure(project_path)