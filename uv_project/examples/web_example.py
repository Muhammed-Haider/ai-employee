"""Example usage of web skills."""

import sys
import os

# Add project root to path to import skills
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from skills.web_skills import http_client, web_scraper, api_client

    print("=== Web Skills Examples ===\n")

    # Note: Web skills require external libraries
    print("Note: Web skills require 'requests' and 'beautifulsoup4' libraries.")
    print("Install with: pip install requests beautifulsoup4\n")

    # Example URL (using a public API for testing)
    test_url = "https://httpbin.org/get"

    # HTTP client examples
    print("HTTP Client Operations:")

    try:
        # Simple GET request
        print(f"  Making GET request to: {test_url}")
        response = http_client.get(test_url, timeout=5)
        print(f"  Status Code: {response.status_code}")
        print(f"  Response Type: {type(response.json())}")
        print("  Success!\n")

        # POST request example
        post_url = "https://httpbin.org/post"
        print(f"  Making POST request to: {post_url}")
        post_response = http_client.post(
            post_url,
            json_data={"message": "Hello from UV Skills"},
            timeout=5
        )
        print(f"  Status Code: {post_response.status_code}")
        print("  Success!\n")

    except ImportError as e:
        print(f"  Error: {e}")
        print("  Make sure 'requests' library is installed.\n")
    except Exception as e:
        print(f"  Error making request: {e}\n")

    # Web scraping examples
    print("Web Scraping Operations:")

    try:
        # Simple scraping example (using a simple test page)
        scrape_url = "https://httpbin.org/html"
        print(f"  Scraping: {scrape_url}")

        soup = web_scraper.scrape_url(scrape_url, timeout=5)
        print(f"  Page title: {soup.title.string if soup.title else 'No title'}")

        # Extract text
        text = web_scraper.extract_text(scrape_url, timeout=5)
        print(f"  Extracted text (first 200 chars): {text[:200]}...\n")

    except ImportError as e:
        print(f"  Error: {e}")
        print("  Make sure 'beautifulsoup4' library is installed.\n")
    except Exception as e:
        print(f"  Error scraping: {e}\n")

    # API client examples
    print("API Client Operations:")

    try:
        # Create an API client
        base_url = "https://jsonplaceholder.typicode.com"
        client = api_client.JSONAPIClient(base_url, timeout=5)

        # Get posts
        print(f"  Fetching posts from: {base_url}")
        posts = client.get_json("/posts")
        print(f"  Retrieved {len(posts)} posts")
        if posts:
            print(f"  First post title: {posts[0]['title'][:50]}...")

        # Get a specific post
        print(f"\n  Fetching post #1")
        post = client.get_json("/posts/1")
        print(f"  Post title: {post['title']}")
        print(f"  Author ID: {post['userId']}")

        # Create a new post (simulated - won't actually create on server)
        print(f"\n  Creating new post (simulated)")
        new_post = {
            "title": "UV Skills Test",
            "body": "Testing API client from UV Skills",
            "userId": 1
        }
        # Note: This will return the simulated response from jsonplaceholder
        created = client.post_json("/posts", data=new_post)
        print(f"  Created post with ID: {created.get('id', 'simulated')}")

    except ImportError as e:
        print(f"  Error: {e}")
        print("  Make sure 'requests' library is installed.")
    except Exception as e:
        print(f"  Error with API client: {e}")

    print("\n=== Web Skills Examples Complete ===")
    print("\nNote: These examples use public test APIs (httpbin.org, jsonplaceholder.typicode.com)")
    print("For real web scraping, you may need to handle rate limiting, authentication,")
    print("and respect robots.txt files.")

except ImportError as e:
    print(f"Error importing web skills: {e}")
    print("Make sure you're running from the project root directory.")
except Exception as e:
    print(f"Error: {e}")