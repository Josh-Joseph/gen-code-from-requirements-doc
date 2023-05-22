from pathlib import Path
import shutil


def create_directory_structure(project_path: Path):
    project_root = project_path / "local_discord_bot"
    
    if project_root.exists():
        shutil.rmtree(project_root)
    
    project_root.mkdir(parents=True, exist_ok=True)
    
    # Create set_up_and_run_bot.sh
    (project_root / "set_up_and_run_bot.sh").touch()
    
    # Create src directory and its files
    src_dir = project_root / "src"
    src_dir.mkdir(parents=True, exist_ok=True)
    (src_dir / "bot.py").touch()
    (src_dir / "utils.py").touch()
    
    # Create requirements.txt, readme.md, and LICENSE
    (project_root / "requirements.txt").touch()
    (project_root / "readme.md").touch()
    (project_root / "LICENSE").touch()


if __name__ == "__main__":
    project_path = Path("generated_projects/local_discord_bot")
    create_directory_structure(project_path)