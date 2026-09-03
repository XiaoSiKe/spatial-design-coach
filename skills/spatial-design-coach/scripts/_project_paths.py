"""Shared path checks for the assignment files managed by this Skill."""

from __future__ import annotations

from pathlib import Path


def sandbox_root(root: Path) -> Path:
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"sandbox root is not a directory: {root}")
    if root in {Path("/").resolve(), Path.home().resolve()}:
        raise ValueError("refusing to use a broad system or home directory")
    return root


def checked_path(root: Path, relative: str, *, directory: bool = False) -> Path:
    """Reject links and type conflicts before creating or using a managed path."""
    parts = Path(relative).parts
    if not parts or Path(relative).is_absolute() or ".." in parts:
        raise ValueError(f"managed path must stay inside the sandbox: {relative}")
    path = root
    for index, part in enumerate(parts):
        path = path / part
        if path.is_symlink():
            raise ValueError(f"managed path must not be a symbolic link: {path}")
        is_directory = directory or index < len(parts) - 1
        if path.exists() and not (path.is_dir() if is_directory else path.is_file()):
            expected = "directory" if is_directory else "file"
            raise ValueError(f"managed path is not a {expected}: {path}")
    return path
