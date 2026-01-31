import asyncio
import os
from datetime import datetime
from playwright.async_api import async_playwright

async def post_to_x_async(text: str) -> dict:
    """
    Posts text to X using Playwright and a saved session.
    Returns: {post_id, post_url, timestamp, success}
    """
    session_path = "x_session.json"
    if not os.path.exists(session_path):
        return {"success": False, "error": "No session found. Run capture_x_session.py first."}

    async with async_playwright() as p:
        # Launch headless browser
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=session_path)
        page = await context.new_page()
        
        try:
            await page.goto("https://x.com/compose/tweet")
            
            # Wait for text area and type
            # X uses a contenteditable div for the tweet box
            tweet_box_selector = 'div[data-testid="tweetTextarea_0"]'
            await page.wait_for_selector(tweet_box_selector)
            await page.click(tweet_box_selector)
            await page.fill(tweet_box_selector, text)
            
            # Click Post button
            post_button_selector = 'button[data-testid="tweetButtonInline"]'
            await page.click(post_button_selector)
            
            # Wait for navigation or success toast
            await page.wait_for_timeout(3000) # Small wait to ensure post is sent
            
            timestamp = datetime.now().isoformat()
            
            # Take screenshot for proof
            screenshot_path = f"screenshots/x_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            os.makedirs("screenshots", exist_ok=True)
            await page.screenshot(path=screenshot_path)
            
            return {
                "success": True,
                "timestamp": timestamp,
                "screenshot": screenshot_path,
                "text": text
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            await browser.close()

def post_to_x(text: str) -> dict:
    """Synchronous wrapper for the async post function."""
    return asyncio.run(post_to_x_async(text))

if __name__ == "__main__":
    # Test (requires session)
    res = post_to_x("Testing the automated poster.")
    print(res)
