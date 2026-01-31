"""Example usage of file skills."""

import sys
import os
import tempfile
from pathlib import Path

# Add project root to path to import skills
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from skills.file_skills import file_ops, directory_ops, search

    print("=== File Skills Examples ===\n")

    # Create a temporary directory for examples
    temp_dir = tempfile.mkdtemp(prefix="uv_skills_example_")
    print(f"Created temporary directory: {temp_dir}\n")

    # File operations examples
    print("File Operations:")

    # Create and write a file
    test_file = Path(temp_dir) / "test.txt"
    content = "Hello, UV Skills!\nThis is a test file.\n"
    file_ops.write_file(test_file, content)
    print(f"  Created file: {test_file}")

    # Read the file
    read_content = file_ops.read_file(test_file)
    print(f"  File content:\n{read_content}")

    # Copy the file
    copied_file = Path(temp_dir) / "test_copy.txt"
    file_ops.copy_file(test_file, copied_file)
    print(f"  Copied to: {copied_file}")

    # Directory operations examples
    print("\nDirectory Operations:")

    # Create a subdirectory
    subdir = Path(temp_dir) / "subdir"
    directory_ops.create_directory(subdir)
    print(f"  Created directory: {subdir}")

    # Create another file in subdirectory
    subdir_file = subdir / "nested.txt"
    file_ops.write_file(subdir_file, "Nested file content")
    print(f"  Created nested file: {subdir_file}")

    # List directory contents
    print(f"\n  Contents of {temp_dir}:")
    items = directory_ops.list_directory(temp_dir)
    for item in items:
        print(f"    {item.name}")

    # Search examples
    print("\nSearch Operations:")

    # Find all .txt files
    txt_files = search.find_files(temp_dir, "*.txt", recursive=True)
    print(f"  Found {len(txt_files)} .txt files:")
    for file in txt_files:
        print(f"    {file}")

    # Search for text in files
    print(f"\n  Searching for 'test' in files:")
    results = search.find_in_files(temp_dir, "test", file_pattern="*.txt", recursive=True)
    for result in results:
        print(f"    File: {result['file'].name}")
        for match in result['matches']:
            print(f"      Line {match['line_number']}: {match['line']}")

    # Cleanup
    print(f"\nCleaning up temporary directory: {temp_dir}")
    directory_ops.delete_directory(temp_dir, recursive=True)
    print("Done!")

except ImportError as e:
    print(f"Error importing file skills: {e}")
    print("Make sure you're running from the project root directory.")
except Exception as e:
    print(f"Error: {e}")
    # Try to clean up temp directory if it exists
    if 'temp_dir' in locals() and Path(temp_dir).exists():
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)