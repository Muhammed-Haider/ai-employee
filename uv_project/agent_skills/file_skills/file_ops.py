"""File operations."""

import os
import shutil
from pathlib import Path
from typing import Union, Optional

def read_file(filepath: Union[str, Path], encoding: str = 'utf-8') -> str:
    """Read the contents of a file.

    Args:
        filepath: Path to the file to read
        encoding: File encoding (default: utf-8)

    Returns:
        File contents as string

    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If there's an error reading the file
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    try:
        with open(filepath, 'r', encoding=encoding) as f:
            return f.read()
    except Exception as e:
        raise IOError(f"Error reading file {filepath}: {e}")

def write_file(
    filepath: Union[str, Path],
    content: str,
    encoding: str = 'utf-8',
    overwrite: bool = True
) -> None:
    """Write content to a file.

    Args:
        filepath: Path to the file to write
        content: Content to write
        encoding: File encoding (default: utf-8)
        overwrite: If True, overwrite existing file. If False, raise error if file exists.

    Raises:
        FileExistsError: If file exists and overwrite=False
        IOError: If there's an error writing the file
    """
    filepath = Path(filepath)

    if filepath.exists() and not overwrite:
        raise FileExistsError(f"File already exists: {filepath}")

    try:
        # Create parent directories if they don't exist
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w', encoding=encoding) as f:
            f.write(content)
    except Exception as e:
        raise IOError(f"Error writing file {filepath}: {e}")

def copy_file(
    source: Union[str, Path],
    destination: Union[str, Path],
    overwrite: bool = False
) -> None:
    """Copy a file from source to destination.

    Args:
        source: Path to source file
        destination: Path to destination file
        overwrite: If True, overwrite existing file at destination

    Raises:
        FileNotFoundError: If source file doesn't exist
        FileExistsError: If destination exists and overwrite=False
        IOError: If there's an error copying the file
    """
    source = Path(source)
    destination = Path(destination)

    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")

    if destination.exists() and not overwrite:
        raise FileExistsError(f"Destination file already exists: {destination}")

    try:
        # Create parent directories if they don't exist
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    except Exception as e:
        raise IOError(f"Error copying file from {source} to {destination}: {e}")

def move_file(
    source: Union[str, Path],
    destination: Union[str, Path],
    overwrite: bool = False
) -> None:
    """Move a file from source to destination.

    Args:
        source: Path to source file
        destination: Path to destination file
        overwrite: If True, overwrite existing file at destination

    Raises:
        FileNotFoundError: If source file doesn't exist
        FileExistsError: If destination exists and overwrite=False
        IOError: If there's an error moving the file
    """
    source = Path(source)
    destination = Path(destination)

    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")

    if destination.exists() and not overwrite:
        raise FileExistsError(f"Destination file already exists: {destination}")

    try:
        # Create parent directories if they don't exist
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(source, destination)
    except Exception as e:
        raise IOError(f"Error moving file from {source} to {destination}: {e}")

def delete_file(filepath: Union[str, Path]) -> None:
    """Delete a file.

    Args:
        filepath: Path to the file to delete

    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If there's an error deleting the file
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    try:
        filepath.unlink()
    except Exception as e:
        raise IOError(f"Error deleting file {filepath}: {e}")