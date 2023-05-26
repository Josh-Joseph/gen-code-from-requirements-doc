import logging
import os
from git import Repo
from datetime import datetime


repo_path = os.getcwd()
repo = Repo(repo_path)
repo_name = repo.working_tree_dir.split('/')[-1]
now = datetime.now()
datetime_str = now.strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"/tmp/logs/{repo_name}/{datetime_str}.log"
os.makedirs(os.path.dirname(log_filename), exist_ok=True)

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s | %(levelname)s | %(message)s",
                    datefmt='%Y-%m-%d %H:%M:%S')

log = logging.getLogger(__name__)

# Create a file handler and add it to the logger
file_handler = logging.FileHandler(log_filename)
file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
log.addHandler(file_handler)

# Create a console handler and add it to the logger
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
log.addHandler(console_handler)
