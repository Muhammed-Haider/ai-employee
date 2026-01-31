"""Web skills module."""

from .http_client import get, post, put, delete, head, options
from .web_scraper import scrape_url, extract_links, extract_text
from .api_client import APIClient, JSONAPIClient

__all__ = [
    'get', 'post', 'put', 'delete', 'head', 'options',
    'scrape_url', 'extract_links', 'extract_text',
    'APIClient', 'JSONAPIClient'
]