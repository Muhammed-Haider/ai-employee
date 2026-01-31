"""Main entry point for UV Skills."""

import sys
import argparse
from typing import List, Optional

def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for UV Skills CLI.

    Args:
        args: Command line arguments (uses sys.argv if None)

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="UV Skills - A collection of useful Python skills",
        prog="uv-skills"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="UV Skills 0.1.0"
    )

    # Create subparsers for different skill categories
    subparsers = parser.add_subparsers(
        dest="category",
        help="Skill category"
    )

    # Math skills subparser
    math_parser = subparsers.add_parser(
        "math",
        help="Math skills"
    )
    math_parser.add_argument(
        "operation",
        choices=["add", "subtract", "multiply", "divide", "mean", "median", "mode"],
        help="Math operation to perform"
    )
    math_parser.add_argument(
        "numbers",
        nargs="+",
        type=float,
        help="Numbers to operate on"
    )

    # File skills subparser
    file_parser = subparsers.add_parser(
        "file",
        help="File skills"
    )
    file_parser.add_argument(
        "operation",
        choices=["read", "write", "list", "search"],
        help="File operation to perform"
    )
    file_parser.add_argument(
        "path",
        help="File or directory path"
    )
    file_parser.add_argument(
        "--content",
        help="Content to write (for write operation)"
    )
    file_parser.add_argument(
        "--pattern",
        help="Search pattern (for search operation)"
    )

    # Web skills subparser
    web_parser = subparsers.add_parser(
        "web",
        help="Web skills"
    )
    web_parser.add_argument(
        "operation",
        choices=["fetch", "links", "text"],
        help="Web operation to perform"
    )
    web_parser.add_argument(
        "url",
        help="URL to process"
    )

    # Parse arguments
    parsed_args = parser.parse_args(args)

    # If no category specified, show help
    if not parsed_args.category:
        parser.print_help()
        return 0

    try:
        # Import here to avoid circular imports
        from ..skills.math_skills import calculator, statistics
        from ..skills.file_skills import file_ops, directory_ops, search
        from ..skills.web_skills import http_client, web_scraper

        if parsed_args.category == "math":
            return _handle_math_operation(parsed_args)
        elif parsed_args.category == "file":
            return _handle_file_operation(parsed_args)
        elif parsed_args.category == "web":
            return _handle_web_operation(parsed_args)
        else:
            print(f"Unknown category: {parsed_args.category}")
            return 1

    except ImportError as e:
        print(f"Error: Required module not available: {e}")
        print("Make sure all dependencies are installed.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

def _handle_math_operation(args) -> int:
    """Handle math operations."""
    operation = args.operation
    numbers = args.numbers

    try:
        if operation == "add":
            result = calculator.add(numbers[0], numbers[1])
        elif operation == "subtract":
            result = calculator.subtract(numbers[0], numbers[1])
        elif operation == "multiply":
            result = calculator.multiply(numbers[0], numbers[1])
        elif operation == "divide":
            result = calculator.divide(numbers[0], numbers[1])
        elif operation == "mean":
            result = statistics.mean(numbers)
        elif operation == "median":
            result = statistics.median(numbers)
        elif operation == "mode":
            result = statistics.mode(numbers)
        else:
            print(f"Unknown math operation: {operation}")
            return 1

        print(f"Result: {result}")
        return 0

    except ZeroDivisionError as e:
        print(f"Error: {e}")
        return 1
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Error performing {operation}: {e}")
        return 1

def _handle_file_operation(args) -> int:
    """Handle file operations."""
    operation = args.operation
    path = args.path

    try:
        if operation == "read":
            content = file_ops.read_file(path)
            print(content)
        elif operation == "write":
            if not args.content:
                print("Error: --content argument required for write operation")
                return 1
            file_ops.write_file(path, args.content)
            print(f"File written: {path}")
        elif operation == "list":
            items = directory_ops.list_directory(path)
            for item in items:
                print(item)
        elif operation == "search":
            if not args.pattern:
                print("Error: --pattern argument required for search operation")
                return 1
            results = search.find_in_files(path, args.pattern)
            for result in results:
                print(f"\nFile: {result['file']}")
                for match in result['matches']:
                    print(f"  Line {match['line_number']}: {match['line']}")
        else:
            print(f"Unknown file operation: {operation}")
            return 1

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Error performing {operation}: {e}")
        return 1

def _handle_web_operation(args) -> int:
    """Handle web operations."""
    operation = args.operation
    url = args.url

    try:
        if operation == "fetch":
            response = http_client.get(url)
            print(f"Status: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            print(f"\nContent (first 1000 chars):\n{response.text[:1000]}...")
        elif operation == "links":
            links = web_scraper.extract_links(url)
            for link in links:
                print(f"{link['text']}: {link['url']}")
        elif operation == "text":
            text = web_scraper.extract_text(url)
            print(text[:2000] + "..." if len(text) > 2000 else text)
        else:
            print(f"Unknown web operation: {operation}")
            return 1

        return 0

    except ImportError as e:
        print(f"Error: {e}")
        print("Web skills require 'requests' and 'beautifulsoup4' libraries.")
        print("Install with: pip install requests beautifulsoup4")
        return 1
    except Exception as e:
        print(f"Error performing {operation}: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())