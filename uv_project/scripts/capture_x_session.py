import asyncio
from playwright.async_api import async_playwright
import os

async def capture_session():
    print("Starting browser for manual login...")
    async with async_playwright() as p:
        # Launch browser in headed mode so you can login
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        await page.goto("https://x.com/i/flow/login")
        
        print("\n!!! ACTION REQUIRED !!!")
        print("Please log in to your X account in the opened browser window.")
        print("Once you are logged in and see your home feed, come back here.")
        
        input("\nPress Enter here AFTER you have successfully logged in and are on the X home page...")
        
        # Save storage state (cookies, etc.)
        await context.storage_state(path="x_session.json")
        print("Session saved to x_session.json")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_session())
