"""Directory operations."""

import os
import shutil
from pathlib import Path
from typing import List, Union, Optional

def list_directory(
    directory: Union[str, Path],
    recursive: bool = False,
    include_hidden: bool = False
) -> List[Path]:
    """List files and directories in a directory.

    Args:
        directory: Path to directory to list
        recursive: If True, list recursively
        include_hidden: If True, include hidden files/directories

    Returns:
        List of Path objects for files and directories

    Raises:
        FileNotFoundError: If directory doesn't exist
        NotADirectoryError: If path is not a directory
    """
    directory = Path(directory)

    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {directory}")

    if recursive:
        items = []
        for root, dirs, files in os.walk(directory):
            root_path = Path(root)

            # Filter hidden files/dirs if needed
            if not include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                files = [f for f in files if not f.startswith('.')]

            # Add directories
            for dir_name in dirs:
                items.append(root_path / dir_name)

            # Add files
            for file_name in files:
                items.append(root_path / file_name)
        return items
    else:
        items = []
        for item in directory.iterdir():
            if not include_hidden and item.name.startswith('.'):
                continue
            items.append(item)
        return items

def create_directory(
    directory: Union[str, Path],
    parents: bool = True,
    exist_ok: bool = True
) -> Path:
    """Create a directory.

    Args:
        directory: Path to directory to create
        parents: If True, create parent directories if they don't exist
        exist_ok: If True, don't raise error if directory already exists

    Returns:
        Path to created directory

    Raises:
        FileExistsError: If directory exists and exist_ok=False
        IOError: If there's an error creating the directory
    """
    directory = Path(directory)

    try:
        directory.mkdir(parents=parents, exist_ok=exist_ok)
        return directory
    except FileExistsError:
        if not exist_ok:
            raise FileExistsError(f"Directory already exists: {directory}")
        return directory
    except Exception as e:
        raise IOError(f"Error creating directory {directory}: {e}")

def delete_directory(
    directory: Union[str, Path],
    recursive: bool = False
) -> None:
    """Delete a directory.

    Args:
        directory: Path to directory to delete
        recursive: If True, delete directory and all its contents

    Raises:
        FileNotFoundError: If directory doesn't exist
        NotADirectoryError: If path is not a directory
        OSError: If directory is not empty and recursive=False
        IOError: If there's an error deleting the directory
    """
    directory = Path(directory)

    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {directory}")

    try:
        if recursive:
            shutil.rmtree(directory)
        else:
            directory.rmdir()
    except OSError as e:
        if not recursive and e.errno == 39:  # Directory not empty
            raise OSError(f"Directory not empty: {directory}. Use recursive=True to delete contents.")
        raise IOError(f"Error deleting directory {directory}: {e}")
    except Exception as e:
        raise IOError(f"Error deleting directory {directory}: {e}")

def get_directory_size(
    directory: Union[str, Path],
    recursive: bool = True
) -> int:
    """Get the total size of a directory in bytes.

    Args:
        directory: Path to directory
        recursive: If True, include sizes of all subdirectories

    Returns:
        Total size in bytes

    Raises:
        FileNotFoundError: If directory doesn't exist
        NotADirectoryError: If path is not a directory
    """
    directory = Path(directory)

    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {directory}")

    total_size = 0

    if recursive:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = Path(root) / file
                try:
                    total_size += file_path.stat().st_size
                except (OSError, IOError):
                    # Skip files we can't access
                    continue
    else:
        for item in directory.iterdir():
            try:
                if item.is_file():
                    total_size += item.stat().st_size
                elif item.is_dir():
                    # For non-recursive, don't include subdirectory sizes
                    pass
            except (OSError, IOError):
                # Skip items we can't access
                continue

    return total_size