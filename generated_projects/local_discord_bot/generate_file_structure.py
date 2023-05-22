from pathlib import Path
import shutil

def create_directory_structure(project_path: Path):
    project_root = project_path / "local_discord_bot"

    # Delete the project root directory if it already exists
    if project_root.exists():
        shutil.rmtree(project_root)

    # Create the project root directory
    project_root.mkdir(parents=True, exist_ok=True)

    # Create the set_up_and_run_bot.sh file
    (project_root / "set_up_and_run_bot.sh").touch()

    # Create the src directory and its files
    src_dir = project_root / "src"
    src_dir.mkdir(parents=True, exist_ok=True)
    (src_dir / "bot.py").touch()
    (src_dir / "utils.py").touch()

    # Create the requirements.txt file
    (project_root / "requirements.txt").touch()

    # Create the readme.md file
    (project_root / "readme.md").touch()

    # Create the LICENSE file
    (project_root / "LICENSE").touch()

if __name__ == "__main__":
    project_path = Path("generated_projects/local_discord_bot")
    create_directory_structure(project_path)