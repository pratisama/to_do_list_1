"""
storage.py -- Disk I/O layer for to-do list CLI.

This module handles functions related to interactions with the file system.
It abstracts away the file handling logic, allowing the main application to focus on user interaction and business logic.

Storage format:
- Each to-do list is stored as a text file in the "lists" directory.
- One .txt file per list. Each task separated by ^ with a trailing ^.
"""

import pathlib as pl

BASE_DIR = pl.Path(__file__).parent.parent / "lists"
SESSION_FILE = ".session"


def ensure_base_dir():
    """
    Ensures that the base directory for storing lists exists. If it doesn't, it creates it.
    """
    BASE_DIR.mkdir(parents=True, exist_ok=True)


def _list_path(list_name: str) -> pl.Path:
    """
    Return the full .txt path for a given list name (private).
    """
    return BASE_DIR / f"{list_name}.txt"


def read_list(file_name: str) -> list[str] | None:
    """Reads the list from memory.
    Returns a list of tasks if the file exists, None if it doesn't. If the file is empty, returns an empty list.
    """

    path = _list_path(file_name)
    if not path.exists():
        return None  # type: ignore
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if not content:
        return []
    return content.split("^")[:-1]


def save_list(tasks: list[str], file_name: str) -> None:
    """
    Writes the list to memory.
    Each element is written to a file, separated by '^'.
    Overwrites the file if it already exists.
    """
    ensure_base_dir()
    with open(_list_path(file_name), "w", encoding="utf-8") as f:
        for element in tasks:
            f.write(element + "^")


def list_create(file_name: str) -> bool:
    """
    Create a new empty list file.
    Success: True
    If file already exists: False
    """
    ensure_base_dir()
    path = _list_path(file_name)
    if path.exists():
        return False
    with open(path, "w", encoding="utf-8") as f:
        f.write("")
    return True


def delete_list(file_name) -> bool:
    """
    Deletes the list file from disk.
    Success: True
    If file doesn't exist: False
    """
    path = _list_path(file_name)
    if not path.exists():
        return False
    path.unlink()
    return True


def save_session(list_name: str) -> None:
    """
    Saves the current session to a file.
    """
    ensure_base_dir()
    with open(_list_path(SESSION_FILE), "w", encoding="utf-8") as f:
        f.write(list_name)


def load_session() -> str | None:
    """
    Loads the current session from a file.
    """
    path = _list_path(SESSION_FILE)
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()
