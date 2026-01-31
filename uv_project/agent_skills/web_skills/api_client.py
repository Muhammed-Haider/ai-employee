"""API client utilities.

Note: This module requires the 'requests' library.
Install it with: pip install requests
"""

import json
import time
from typing import Dict, Any, Optional, Union, List
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
            "The 'requests' library is required for API client. "
            "Install it with: pip install requests"
        )

class APIClient:
    """Base API client for making HTTP requests."""

    def __init__(
        self,
        base_url: str,
        default_headers: Optional[Dict[str, str]] = None,
        timeout: int = 10,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        """Initialize API client.

        Args:
            base_url: Base URL for API requests
            default_headers: Default headers for all requests
            timeout: Default timeout in seconds
            max_retries: Maximum number of retries for failed requests
            retry_delay: Delay between retries in seconds
        """
        _check_requests()

        self.base_url = base_url.rstrip('/')
        self.default_headers = default_headers or {}
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # Ensure base URL ends with slash for urljoin to work correctly
        if not self.base_url.endswith('/'):
            self.base_url += '/'

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str, bytes]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs
    ) -> requests.Response:
        """Make an HTTP request with retry logic.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint (relative to base_url)
            params: Query parameters
            data: Form data or raw data
            json_data: JSON data
            headers: Additional headers
            timeout: Request timeout (uses default if None)
            **kwargs: Additional arguments passed to requests.request

        Returns:
            Response object

        Raises:
            RequestException: If request fails after all retries
        """
        url = urljoin(self.base_url, endpoint.lstrip('/'))

        # Merge headers
        request_headers = self.default_headers.copy()
        if headers:
            request_headers.update(headers)

        # Use provided timeout or default
        request_timeout = timeout if timeout is not None else self.timeout

        last_exception = None
        for attempt in range(self.max_retries):
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    json=json_data,
                    headers=request_headers,
                    timeout=request_timeout,
                    **kwargs
                )
                response.raise_for_status()
                return response

            except (Timeout, ConnectionError) as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise RequestException(
                        f"Request to {url} failed after {self.max_retries} attempts: {e}"
                    )
            except HTTPError as e:
                # Don't retry on HTTP errors (4xx, 5xx) except 429 (Too Many Requests)
                if e.response.status_code == 429 and attempt < self.max_retries - 1:
                    # Rate limited - wait and retry
                    retry_after = e.response.headers.get('Retry-After')
                    if retry_after:
                        try:
                            delay = float(retry_after)
                        except ValueError:
                            delay = self.retry_delay * (attempt + 1)
                    else:
                        delay = self.retry_delay * (attempt + 1)

                    time.sleep(delay)
                    last_exception = e
                    continue
                else:
                    raise e
            except RequestException as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise RequestException(
                        f"Request to {url} failed after {self.max_retries} attempts: {e}"
                    )

        # This should never be reached, but just in case
        raise RequestException(
            f"Request to {url} failed after {self.max_retries} attempts: {last_exception}"
        )

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs
    ) -> requests.Response:
        """Send a GET request.

        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Additional headers
            timeout: Request timeout
            **kwargs: Additional arguments

        Returns:
            Response object
        """
        return self._make_request(
            'GET', endpoint, params=params, headers=headers, timeout=timeout, **kwargs
        )

    def post(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str, bytes]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs
    ) -> requests.Response:
        """Send a POST request.

        Args:
            endpoint: API endpoint
            data: Form data or raw data
            json_data: JSON data
            headers: Additional headers
            timeout: Request timeout
            **kwargs: Additional arguments

        Returns:
            Response object
        """
        return self._make_request(
            'POST', endpoint, data=data, json_data=json_data,
            headers=headers, timeout=timeout, **kwargs
        )

    def put(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str, bytes]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs
    ) -> requests.Response:
        """Send a PUT request.

        Args:
            endpoint: API endpoint
            data: Form data or raw data
            json_data: JSON data
            headers: Additional headers
            timeout: Request timeout
            **kwargs: Additional arguments

        Returns:
            Response object
        """
        return self._make_request(
            'PUT', endpoint, data=data, json_data=json_data,
            headers=headers, timeout=timeout, **kwargs
        )

    def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs
    ) -> requests.Response:
        """Send a DELETE request.

        Args:
            endpoint: API endpoint
            headers: Additional headers
            timeout: Request timeout
            **kwargs: Additional arguments

        Returns:
            Response object
        """
        return self._make_request(
            'DELETE', endpoint, headers=headers, timeout=timeout, **kwargs
        )

    def patch(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str, bytes]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs
    ) -> requests.Response:
        """Send a PATCH request.

        Args:
            endpoint: API endpoint
            data: Form data or raw data
            json_data: JSON data
            headers: Additional headers
            timeout: Request timeout
            **kwargs: Additional arguments

        Returns:
            Response object
        """
        return self._make_request(
            'PATCH', endpoint, data=data, json_data=json_data,
            headers=headers, timeout=timeout, **kwargs
        )


class JSONAPIClient(APIClient):
    """API client that automatically handles JSON serialization/deserialization."""

    def __init__(
        self,
        base_url: str,
        default_headers: Optional[Dict[str, str]] = None,
        timeout: int = 10,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        """Initialize JSON API client.

        Args:
            base_url: Base URL for API requests
            default_headers: Default headers for all requests
            timeout: Default timeout in seconds
            max_retries: Maximum number of retries for failed requests
            retry_delay: Delay between retries in seconds
        """
        # Set JSON content type header
        headers = default_headers or {}
        headers.setdefault('Content-Type', 'application/json')
        headers.setdefault('Accept', 'application/json')

        super().__init__(base_url, headers, timeout, max_retries, retry_delay)

    def get_json(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs
    ) -> Any:
        """Send GET request and return parsed JSON.

        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Additional headers
            timeout: Request timeout
            **kwargs: Additional arguments

        Returns:
            Parsed JSON response
        """
        response = self.get(endpoint, params, headers, timeout, **kwargs)
        return response.json()

    def post_json(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs
    ) -> Any:
        """Send POST request with JSON data and return parsed JSON.

        Args:
            endpoint: API endpoint
            data: JSON data to send
            headers: Additional headers
            timeout: Request timeout
            **kwargs: Additional arguments

        Returns:
            Parsed JSON response
        """
        response = self.post(endpoint, json_data=data, headers=headers, timeout=timeout, **kwargs)
        return response.json()

    def put_json(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs
    ) -> Any:
        """Send PUT request with JSON data and return parsed JSON.

        Args:
            endpoint: API endpoint
            data: JSON data to send
            headers: Additional headers
            timeout: Request timeout
            **kwargs: Additional arguments

        Returns:
            Parsed JSON response
        """
        response = self.put(endpoint, json_data=data, headers=headers, timeout=timeout, **kwargs)
        return response.json()

    def patch_json(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs
    ) -> Any:
        """Send PATCH request with JSON data and return parsed JSON.

        Args:
            endpoint: API endpoint
            data: JSON data to send
            headers: Additional headers
            timeout: Request timeout
            **kwargs: Additional arguments

        Returns:
            Parsed JSON response
        """
        response = self.patch(endpoint, json_data=data, headers=headers, timeout=timeout, **kwargs)
        return response.json()

    def delete_json(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs
    ) -> Any:
        """Send DELETE request and return parsed JSON.

        Args:
            endpoint: API endpoint
            headers: Additional headers
            timeout: Request timeout
            **kwargs: Additional arguments

        Returns:
            Parsed JSON response
        """
        response = self.delete(endpoint, headers, timeout, **kwargs)
        # Some APIs return empty response for DELETE
        if response.content:
            return response.json()
        return None