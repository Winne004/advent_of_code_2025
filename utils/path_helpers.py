import sys
from pathlib import Path


def add_project_root_to_path() -> None:
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
