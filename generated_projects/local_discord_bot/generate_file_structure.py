#!/usr/bin/env python3

from pathlib import Path
import shutil


def create_directory_structure(project_root: Path):
    if project_root.exists():
        shutil.rmtree(project_root)

    project_root.mkdir(parents=True, exist_ok=True)

    # Create directories
    (project_root / "src").mkdir()
    (project_root / "tests").mkdir()

    # Create files
    (project_root / "LICENSE").touch()
    (project_root / "readme.md").touch()
    (project_root / "requirements.txt").touch()
    (project_root / "set_up_and_run_bot.sh").touch(mode=0o755)
    (project_root / "src" / "bot.py").touch()
    (project_root / "tests" / "test_bot.py").touch()


if __name__ == "__main__":
    project_root = Path("generated_projects/local_discord_bot/local_discord_bot")
    create_directory_structure(project_root)