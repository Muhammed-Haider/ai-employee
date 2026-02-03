import asyncio
import os
from playwright.async_api import async_playwright

async def capture_linkedin_session():
    """
    Opens a browser for manual LinkedIn login and saves the session state.
    """
    print("Starting browser for manual LinkedIn login...")
    async with async_playwright() as p:
        # Launch browser in headed mode for manual interaction
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        await page.goto("https://www.linkedin.com/login")
        
        print("\n!!! ACTION REQUIRED !!!")
        print("1. Log in to your LinkedIn account manually in the browser window.")
        print("2. Once you see your feed and unread notifications, return here.")
        
        input("\nPress Enter AFTER you have logged in and are on the LinkedIn home page...")
        
        # Save storage state (cookies, session, etc.)
        session_path = "linkedin_session.json"
        await context.storage_state(path=session_path)
        
        print(f"SUCCESS: LinkedIn session saved to {os.path.abspath(session_path)}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_linkedin_session())

