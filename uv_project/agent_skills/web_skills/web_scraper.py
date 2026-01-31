"""Web scraping utilities.

Note: This module requires the 'requests' and 'beautifulsoup4' libraries.
Install with: pip install requests beautifulsoup4
"""

from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
    REQUESTS_AVAILABLE = True
    BEAUTIFULSOUP_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    BEAUTIFULSOUP_AVAILABLE = False

def _check_dependencies():
    """Check if required libraries are available."""
    if not REQUESTS_AVAILABLE:
        raise ImportError(
            "The 'requests' library is required for web scraping. "
            "Install it with: pip install requests"
        )
    if not BEAUTIFULSOUP_AVAILABLE:
        raise ImportError(
            "The 'beautifulsoup4' library is required for web scraping. "
            "Install it with: pip install beautifulsoup4"
        )

def scrape_url(
    url: str,
    timeout: int = 10,
    headers: Optional[Dict[str, str]] = None,
    **kwargs
) -> BeautifulSoup:
    """Scrape a URL and return BeautifulSoup object.

    Args:
        url: URL to scrape
        timeout: Request timeout in seconds
        headers: HTTP headers to send
        **kwargs: Additional arguments passed to requests.get

    Returns:
        BeautifulSoup object for parsed HTML

    Raises:
        ImportError: If required libraries are not installed
        RequestException: If request fails
        ValueError: If HTML cannot be parsed
    """
    _check_dependencies()

    # Default headers to mimic a browser
    default_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    if headers:
        default_headers.update(headers)

    try:
        response = requests.get(url, timeout=timeout, headers=default_headers, **kwargs)
        response.raise_for_status()

        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Failed to scrape {url}: {e}")
    except Exception as e:
        raise ValueError(f"Failed to parse HTML from {url}: {e}")

def extract_links(
    url: str,
    same_domain: bool = True,
    timeout: int = 10,
    **kwargs
) -> List[Dict[str, str]]:
    """Extract all links from a webpage.

    Args:
        url: URL to extract links from
        same_domain: If True, only return links from the same domain
        timeout: Request timeout in seconds
        **kwargs: Additional arguments passed to scrape_url

    Returns:
        List of dictionaries with link text and URL

    Raises:
        ImportError: If required libraries are not installed
        RequestException: If request fails
    """
    _check_dependencies()

    try:
        soup = scrape_url(url, timeout=timeout, **kwargs)

        # Get base domain for filtering
        base_domain = urlparse(url).netloc if same_domain else None

        links = []
        for a_tag in soup.find_all('a', href=True):
            link_text = a_tag.get_text(strip=True)
            link_url = a_tag['href']

            # Convert relative URLs to absolute
            if not link_url.startswith(('http://', 'https://')):
                link_url = urljoin(url, link_url)

            # Filter by domain if requested
            if same_domain and base_domain:
                link_domain = urlparse(link_url).netloc
                if link_domain != base_domain:
                    continue

            links.append({
                'text': link_text,
                'url': link_url
            })

        return links

    except Exception as e:
        raise Exception(f"Failed to extract links from {url}: {e}")

def extract_text(
    url: str,
    selector: Optional[str] = None,
    timeout: int = 10,
    **kwargs
) -> str:
    """Extract text content from a webpage.

    Args:
        url: URL to extract text from
        selector: CSS selector to extract specific element(s)
        timeout: Request timeout in seconds
        **kwargs: Additional arguments passed to scrape_url

    Returns:
        Extracted text content

    Raises:
        ImportError: If required libraries are not installed
        RequestException: If request fails
    """
    _check_dependencies()

    try:
        soup = scrape_url(url, timeout=timeout, **kwargs)

        if selector:
            # Extract text from specific element(s)
            elements = soup.select(selector)
            texts = [elem.get_text(strip=True) for elem in elements]
            return ' '.join(texts)
        else:
            # Extract all text
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text and normalize whitespace
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)

            return text

    except Exception as e:
        raise Exception(f"Failed to extract text from {url}: {e}")

def extract_images(
    url: str,
    same_domain: bool = True,
    timeout: int = 10,
    **kwargs
) -> List[Dict[str, str]]:
    """Extract all images from a webpage.

    Args:
        url: URL to extract images from
        same_domain: If True, only return images from the same domain
        timeout: Request timeout in seconds
        **kwargs: Additional arguments passed to scrape_url

    Returns:
        List of dictionaries with image alt text and URL

    Raises:
        ImportError: If required libraries are not installed
        RequestException: If request fails
    """
    _check_dependencies()

    try:
        soup = scrape_url(url, timeout=timeout, **kwargs)

        # Get base domain for filtering
        base_domain = urlparse(url).netloc if same_domain else None

        images = []
        for img_tag in soup.find_all('img', src=True):
            alt_text = img_tag.get('alt', '')
            img_url = img_tag['src']

            # Convert relative URLs to absolute
            if not img_url.startswith(('http://', 'https://', 'data:')):
                img_url = urljoin(url, img_url)

            # Filter by domain if requested
            if same_domain and base_domain and not img_url.startswith('data:'):
                img_domain = urlparse(img_url).netloc
                if img_domain != base_domain:
                    continue

            images.append({
                'alt': alt_text,
                'url': img_url
            })

        return images

    except Exception as e:
        raise Exception(f"Failed to extract images from {url}: {e}")

def extract_metadata(
    url: str,
    timeout: int = 10,
    **kwargs
) -> Dict[str, str]:
    """Extract metadata from a webpage.

    Args:
        url: URL to extract metadata from
        timeout: Request timeout in seconds
        **kwargs: Additional arguments passed to scrape_url

    Returns:
        Dictionary of metadata (title, description, keywords, etc.)

    Raises:
        ImportError: If required libraries are not installed
        RequestException: If request fails
    """
    _check_dependencies()

    try:
        soup = scrape_url(url, timeout=timeout, **kwargs)

        metadata = {}

        # Title
        title_tag = soup.find('title')
        if title_tag:
            metadata['title'] = title_tag.get_text(strip=True)

        # Meta tags
        meta_tags = soup.find_all('meta')
        for meta in meta_tags:
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                metadata[name.lower()] = content

        # Open Graph tags
        og_tags = {}
        for meta in meta_tags:
            property_attr = meta.get('property', '')
            if property_attr.startswith('og:'):
                og_tags[property_attr[3:]] = meta.get('content', '')
        if og_tags:
            metadata['opengraph'] = og_tags

        return metadata

    except Exception as e:
        raise Exception(f"Failed to extract metadata from {url}: {e}")