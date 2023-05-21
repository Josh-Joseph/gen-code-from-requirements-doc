from pathlib import Path
import shutil


def create_directory_structure(project_path: Path) -> None:
    project_root = project_path / "discord_character_counter"

    if project_root.exists():
        shutil.rmtree(project_root)

    project_root.mkdir(parents=True, exist_ok=True)

    # Create directories
    (project_root / ".github" / "workflows").mkdir(parents=True, exist_ok=True)
    (project_root / "src").mkdir(parents=True, exist_ok=True)

    # Create files
    (project_root / ".github" / "workflows" / "deploy.yaml").touch()
    (project_root / "src" / "discord_bot.py").touch()
    (project_root / "src" / "run_bot.py").touch()
    (project_root / ".gitignore").touch()
    (project_root / "LICENSE").touch()
    (project_root / "README.md").touch()
    (project_root / "requirements.txt").touch()
    (project_root / "project_design_document.md").touch()


if __name__ == "__main__":
    project_path = Path("generated_projects/discord_bot")
    create_directory_structure(project_path)