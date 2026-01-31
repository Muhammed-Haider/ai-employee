"""File search utilities."""

import os
import fnmatch
from pathlib import Path
from typing import List, Union, Optional, Pattern
import re

def find_files(
    directory: Union[str, Path],
    pattern: str = "*",
    recursive: bool = True,
    case_sensitive: bool = False
) -> List[Path]:
    """Find files matching a pattern in a directory.

    Args:
        directory: Directory to search in
        pattern: Glob pattern to match (e.g., "*.py", "test_*.txt")
        recursive: If True, search recursively in subdirectories
        case_sensitive: If True, pattern matching is case-sensitive

    Returns:
        List of Path objects for matching files

    Raises:
        FileNotFoundError: If directory doesn't exist
        NotADirectoryError: If path is not a directory
    """
    directory = Path(directory)

    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {directory}")

    matches = []

    if recursive:
        for root, dirs, files in os.walk(directory):
            root_path = Path(root)
            for file in files:
                file_path = root_path / file

                # Check if file matches pattern
                if case_sensitive:
                    matches_pattern = fnmatch.fnmatch(file, pattern)
                else:
                    matches_pattern = fnmatch.fnmatchcase(file, pattern)

                if matches_pattern:
                    matches.append(file_path)
    else:
        for item in directory.iterdir():
            if item.is_file():
                file_name = item.name

                # Check if file matches pattern
                if case_sensitive:
                    matches_pattern = fnmatch.fnmatch(file_name, pattern)
                else:
                    matches_pattern = fnmatch.fnmatchcase(file_name, pattern)

                if matches_pattern:
                    matches.append(item)

    return matches

def find_in_files(
    directory: Union[str, Path],
    search_text: Union[str, Pattern],
    file_pattern: str = "*",
    recursive: bool = True,
    case_sensitive: bool = False,
    encoding: str = 'utf-8'
) -> List[dict]:
    """Search for text in files.

    Args:
        directory: Directory to search in
        search_text: Text or regex pattern to search for
        file_pattern: Glob pattern to filter files
        recursive: If True, search recursively in subdirectories
        case_sensitive: If True, search is case-sensitive
        encoding: File encoding to use when reading files

    Returns:
        List of dictionaries with file path and line matches

    Raises:
        FileNotFoundError: If directory doesn't exist
        NotADirectoryError: If path is not a directory
    """
    directory = Path(directory)

    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {directory}")

    # Compile regex if search_text is a string
    if isinstance(search_text, str):
        flags = 0 if case_sensitive else re.IGNORECASE
        try:
            pattern = re.compile(search_text, flags)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")
    else:
        pattern = search_text

    results = []

    # First find files matching the pattern
    files_to_search = find_files(directory, file_pattern, recursive, case_sensitive)

    for file_path in files_to_search:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                lines = f.readlines()

            file_matches = []
            for line_num, line in enumerate(lines, 1):
                if pattern.search(line):
                    file_matches.append({
                        'line_number': line_num,
                        'line': line.rstrip('\n'),
                        'match': pattern.search(line).group()
                    })

            if file_matches:
                results.append({
                    'file': file_path,
                    'matches': file_matches
                })

        except (UnicodeDecodeError, IOError):
            # Skip files we can't read (binary files, permission issues, etc.)
            continue
        except Exception as e:
            # Skip files with other errors
            continue

    return results

def find_files_by_extension(
    directory: Union[str, Path],
    extensions: Union[str, List[str]],
    recursive: bool = True
) -> List[Path]:
    """Find files by extension(s).

    Args:
        directory: Directory to search in
        extensions: Single extension (e.g., ".py") or list of extensions (e.g., [".py", ".txt"])
        recursive: If True, search recursively in subdirectories

    Returns:
        List of Path objects for matching files
    """
    if isinstance(extensions, str):
        extensions = [extensions]

    # Ensure extensions start with dot
    extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]

    # Create pattern for all extensions
    pattern = f"*{{{','.join(extensions)}}}"

    return find_files(directory, pattern, recursive, case_sensitive=False)

def find_latest_files(
    directory: Union[str, Path],
    count: int = 10,
    recursive: bool = True
) -> List[Path]:
    """Find the most recently modified files.

    Args:
        directory: Directory to search in
        count: Number of latest files to return
        recursive: If True, search recursively in subdirectories

    Returns:
        List of Path objects for latest files, sorted by modification time (newest first)
    """
    directory = Path(directory)

    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {directory}")

    all_files = []

    if recursive:
        for root, dirs, files in os.walk(directory):
            root_path = Path(root)
            for file in files:
                file_path = root_path / file
                try:
                    mtime = file_path.stat().st_mtime
                    all_files.append((mtime, file_path))
                except (OSError, IOError):
                    # Skip files we can't access
                    continue
    else:
        for item in directory.iterdir():
            if item.is_file():
                try:
                    mtime = item.stat().st_mtime
                    all_files.append((mtime, item))
                except (OSError, IOError):
                    # Skip files we can't access
                    continue

    # Sort by modification time (newest first) and get top N
    all_files.sort(key=lambda x: x[0], reverse=True)
    return [file_path for _, file_path in all_files[:count]]