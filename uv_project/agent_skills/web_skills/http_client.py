"""HTTP client utilities.

Note: This module requires the 'requests' library.
Install it with: pip install requests
"""

import json
from typing import Dict, Any, Optional, Union
from urllib.parse import urljoin

try:
    import requests
    from requests.exceptions import RequestException, Timeout, HTTPError
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

def _check_requests():
    """Check if requests library is available."""
    if not REQUESTS_AVAILABLE:
        raise ImportError(
            "The 'requests' library is required for web skills. "
            "Install it with: pip install requests"
        )

def get(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 10,
    **kwargs
) -> requests.Response:
    """Send a GET request.

    Args:
        url: URL to send request to
        params: Query parameters
        headers: HTTP headers
        timeout: Request timeout in seconds
        **kwargs: Additional arguments passed to requests.get

    Returns:
        Response object

    Raises:
        ImportError: If requests library is not installed
        RequestException: If request fails
    """
    _check_requests()

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=timeout,
            **kwargs
        )
        response.raise_for_status()
        return response
    except Timeout:
        raise Timeout(f"Request to {url} timed out after {timeout} seconds")
    except HTTPError as e:
        raise HTTPError(f"HTTP error for {url}: {e}")
    except RequestException as e:
        raise RequestException(f"Request failed for {url}: {e}")

def post(
    url: str,
    data: Optional[Union[Dict[str, Any], str, bytes]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 10,
    **kwargs
) -> requests.Response:
    """Send a POST request.

    Args:
        url: URL to send request to
        data: Form data or raw data to send
        json_data: JSON data to send (will be serialized)
        headers: HTTP headers
        timeout: Request timeout in seconds
        **kwargs: Additional arguments passed to requests.post

    Returns:
        Response object

    Raises:
        ImportError: If requests library is not installed
        RequestException: If request fails
    """
    _check_requests()

    try:
        response = requests.post(
            url,
            data=data,
            json=json_data,
            headers=headers,
            timeout=timeout,
            **kwargs
        )
        response.raise_for_status()
        return response
    except Timeout:
        raise Timeout(f"Request to {url} timed out after {timeout} seconds")
    except HTTPError as e:
        raise HTTPError(f"HTTP error for {url}: {e}")
    except RequestException as e:
        raise RequestException(f"Request failed for {url}: {e}")

def put(
    url: str,
    data: Optional[Union[Dict[str, Any], str, bytes]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 10,
    **kwargs
) -> requests.Response:
    """Send a PUT request.

    Args:
        url: URL to send request to
        data: Form data or raw data to send
        json_data: JSON data to send (will be serialized)
        headers: HTTP headers
        timeout: Request timeout in seconds
        **kwargs: Additional arguments passed to requests.put

    Returns:
        Response object

    Raises:
        ImportError: If requests library is not installed
        RequestException: If request fails
    """
    _check_requests()

    try:
        response = requests.put(
            url,
            data=data,
            json=json_data,
            headers=headers,
            timeout=timeout,
            **kwargs
        )
        response.raise_for_status()
        return response
    except Timeout:
        raise Timeout(f"Request to {url} timed out after {timeout} seconds")
    except HTTPError as e:
        raise HTTPError(f"HTTP error for {url}: {e}")
    except RequestException as e:
        raise RequestException(f"Request failed for {url}: {e}")

def delete(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 10,
    **kwargs
) -> requests.Response:
    """Send a DELETE request.

    Args:
        url: URL to send request to
        headers: HTTP headers
        timeout: Request timeout in seconds
        **kwargs: Additional arguments passed to requests.delete

    Returns:
        Response object

    Raises:
        ImportError: If requests library is not installed
        RequestException: If request fails
    """
    _check_requests()

    try:
        response = requests.delete(
            url,
            headers=headers,
            timeout=timeout,
            **kwargs
        )
        response.raise_for_status()
        return response
    except Timeout:
        raise Timeout(f"Request to {url} timed out after {timeout} seconds")
    except HTTPError as e:
        raise HTTPError(f"HTTP error for {url}: {e}")
    except RequestException as e:
        raise RequestException(f"Request failed for {url}: {e}")

def head(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 10,
    **kwargs
) -> requests.Response:
    """Send a HEAD request.

    Args:
        url: URL to send request to
        headers: HTTP headers
        timeout: Request timeout in seconds
        **kwargs: Additional arguments passed to requests.head

    Returns:
        Response object

    Raises:
        ImportError: If requests library is not installed
        RequestException: If request fails
    """
    _check_requests()

    try:
        response = requests.head(
            url,
            headers=headers,
            timeout=timeout,
            **kwargs
        )
        response.raise_for_status()
        return response
    except Timeout:
        raise Timeout(f"Request to {url} timed out after {timeout} seconds")
    except HTTPError as e:
        raise HTTPError(f"HTTP error for {url}: {e}")
    except RequestException as e:
        raise RequestException(f"Request failed for {url}: {e}")

def options(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 10,
    **kwargs
) -> requests.Response:
    """Send an OPTIONS request.

    Args:
        url: URL to send request to
        headers: HTTP headers
        timeout: Request timeout in seconds
        **kwargs: Additional arguments passed to requests.options

    Returns:
        Response object

    Raises:
        ImportError: If requests library is not installed
        RequestException: If request fails
    """
    _check_requests()

    try:
        response = requests.options(
            url,
            headers=headers,
            timeout=timeout,
            **kwargs
        )
        response.raise_for_status()
        return response
    except Timeout:
        raise Timeout(f"Request to {url} timed out after {timeout} seconds")
    except HTTPError as e:
        raise HTTPError(f"HTTP error for {url}: {e}")
    except RequestException as e:
        raise RequestException(f"Request failed for {url}: {e}")

def download_file(
    url: str,
    filepath: str,
    timeout: int = 30,
    chunk_size: int = 8192,
    **kwargs
) -> str:
    """Download a file from a URL.

    Args:
        url: URL to download from
        filepath: Local path to save the file
        timeout: Request timeout in seconds
        chunk_size: Size of chunks to download at a time
        **kwargs: Additional arguments passed to requests.get

    Returns:
        Path to downloaded file

    Raises:
        ImportError: If requests library is not installed
        RequestException: If download fails
        IOError: If file cannot be written
    """
    _check_requests()

    try:
        response = requests.get(url, stream=True, timeout=timeout, **kwargs)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)

        return filepath
    except Timeout:
        raise Timeout(f"Download from {url} timed out after {timeout} seconds")
    except HTTPError as e:
        raise HTTPError(f"HTTP error downloading from {url}: {e}")
    except RequestException as e:
        raise RequestException(f"Download failed from {url}: {e}")
    except IOError as e:
        raise IOError(f"Failed to write file {filepath}: {e}")