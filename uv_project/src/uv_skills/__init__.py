"""UV Skills - A collection of useful skills for Python projects."""

__version__ = "0.1.0"
__author__ = "Developer"
__email__ = "dev@example.com"

# Import skills for easy access
try:
    from skills.math_skills import calculator, statistics
    from skills.file_skills import file_ops, directory_ops, search
    from skills.web_skills import http_client, web_scraper, api_client

    # Re-export commonly used functions
    from skills.math_skills.calculator import add, subtract, multiply, divide
    from skills.math_skills.statistics import mean, median, mode, variance, standard_deviation
    from skills.file_skills.file_ops import read_file, write_file, copy_file, move_file, delete_file
    from skills.file_skills.directory_ops import list_directory, create_directory, delete_directory
    from skills.file_skills.search import find_files, find_in_files
    from skills.web_skills.http_client import get, post, put, delete, head, options
    from skills.web_skills.web_scraper import scrape_url, extract_links, extract_text
    from skills.web_skills.api_client import APIClient, JSONAPIClient

    __all__ = [
        # Modules
        'calculator', 'statistics',
        'file_ops', 'directory_ops', 'search',
        'http_client', 'web_scraper', 'api_client',

        # Functions
        'add', 'subtract', 'multiply', 'divide',
        'mean', 'median', 'mode', 'variance', 'standard_deviation',
        'read_file', 'write_file', 'copy_file', 'move_file', 'delete_file',
        'list_directory', 'create_directory', 'delete_directory',
        'find_files', 'find_in_files',
        'get', 'post', 'put', 'delete', 'head', 'options',
        'scrape_url', 'extract_links', 'extract_text',
        'APIClient', 'JSONAPIClient'
    ]

except ImportError as e:
    # Skills might not be available during initial setup
    print(f"Warning: Some skills not available: {e}")
    __all__ = []