from pathlib import Path

_here = Path(__file__)
project_base = _here.parent.parent


def get_path_relative_to_project_root(relative_path: str | Path):
    if isinstance(relative_path, str):
        relative_path = Path(relative_path)
    if relative_path.is_absolute():
        raise ValueError("Absolute path received")
    return project_base / relative_path
