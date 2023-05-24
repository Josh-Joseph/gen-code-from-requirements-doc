from pathlib import Path
import shutil
from typing import List, Tuple


def create_directory_structure(project_root: Path) -> None:
    if project_root.exists():
        shutil.rmtree(project_root)
    
    project_root.mkdir(parents=True, exist_ok=True)
    
    file_structure = [
        (project_root, [".gitignore", "LICENSE", "readme.md", "requirements.txt", "set_up_and_run_bot.sh"]),
        (project_root / "src", ["github_api.py", "main.py"]),
    ]
    
    for directory, files in file_structure:
        directory.mkdir(parents=True, exist_ok=True)
        for file in files:
            (directory / file).touch()
            

if __name__ == "__main__":
    project_root = Path("generated_projects/github_issues_to_pr_bot/github_issues_to_pr_bot")
    create_directory_structure(project_root)