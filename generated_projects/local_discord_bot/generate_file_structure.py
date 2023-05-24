from pathlib import Path
import shutil


def create_directory_structure(project_path: Path) -> None:
    project_root = project_path / "local_discord_bot"
    
    if project_root.exists():
        shutil.rmtree(project_root)
    
    project_root.mkdir(parents=True, exist_ok=True)
    
    # Create directories
    (project_root / "src").mkdir()
    
    # Create files
    (project_root / "set_up_and_run_bot.sh").touch()
    (project_root / "src" / "bot.py").touch()
    (project_root / "src" / "utils.py").touch()
    (project_root / "requirements.txt").touch()
    (project_root / "readme.md").touch()
    (project_root / "LICENSE").touch()


if __name__ == "__main__":
    create_directory_structure(Path("generated_projects/local_discord_bot"))