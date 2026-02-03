import asyncio
import os
from playwright.async_api import async_playwright

import asyncio
import os
import json
import hashlib
from datetime import datetime
from playwright.async_api import async_playwright

class LinkedInWatcher:
    """
    Watches LinkedIn for new activity, such as notifications and messages.
    """
    def __init__(self, session_path="../linkedin_session.json", vault_path="../AI_Employee_Vault/Inbox", cache_path="linkedin_seen.json"):
        # ... (rest of __init__ is unchanged)
        self.session_path = session_path
        self.vault_path = vault_path
        self.cache_path = cache_path
        self.seen_ids = set()

        if not os.path.exists(self.session_path):
            raise FileNotFoundError(
                f"LinkedIn session file not found at '{os.path.abspath(self.session_path)}'. "
                "Please run the `capture_linkedin_session.py` script first."
            )
        os.makedirs(self.vault_path, exist_ok=True)
        self._load_cache()

    def _load_cache(self):
        # ... (method unchanged)
        try:
            if os.path.exists(self.cache_path):
                with open(self.cache_path, 'r', encoding='utf-8') as f:
                    self.seen_ids = set(json.load(f))
                print(f"Loaded {len(self.seen_ids)} seen items from cache.")
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load cache file. Starting fresh. Error: {e}")
            self.seen_ids = set()

    def _update_cache(self):
        # ... (method unchanged)
        try:
            with open(self.cache_path, 'w', encoding='utf-8') as f:
                json.dump(list(self.seen_ids), f, indent=2)
            print(f"Updated cache with {len(self.seen_ids)} seen items.")
        except IOError as e:
            print(f"Error: Could not write to cache file. Error: {e}")

    async def check_notifications(self, page):
        """
        Checks for new notifications and returns them as a list of dictionaries.
        """
        print("Checking for new notifications...")
        await page.goto("https://www.linkedin.com/notifications/")
        
        # Wait for the main notifications container to load
        await page.wait_for_selector('div.scaffold-finite-scroll__content', timeout=60000)

        # Find all notification card articles
        notification_items = await page.query_selector_all('article.nt-card')
        
        notifications = []
        for item in notification_items[:5]:  # Limit to the top 5
            try:
                # Extract the main text from the notification card
                headline_element = await item.query_selector('a.nt-card__headline')
                if headline_element:
                    text = await headline_element.inner_text()
                    notifications.append({"type": "notification", "content": text.strip()})
            except Exception as e:
                print(f"Could not extract text from a notification item: {e}")
        
        print(f"Found {len(notifications)} notifications.")
        return notifications

    async def check_messages(self, page):
        # ... (method unchanged)
        print("Checking for new messages...")
        await page.goto("https://www.linkedin.com/messaging/")
        await page.wait_for_selector('ul.msg-conversations-container__conversations-list', timeout=60000)

        unread_items = await page.query_selector_all('li.msg-conversation-listitem--unread')
        
        messages = []
        for item in unread_items:
            try:
                sender_element = await item.query_selector('h3.msg-conversation-listitem__participant-names')
                snippet_element = await item.query_selector('p.msg-conversation-listitem__snippet')
                
                sender = await sender_element.inner_text() if sender_element else "Unknown Sender"
                snippet = await snippet_element.inner_text() if snippet_element else "No snippet available"
                
                messages.append({
                    "type": "message",
                    "sender": sender.strip(),
                    "snippet": snippet.strip()
                })
            except Exception as e:
                print(f"Could not extract data from a message item: {e}")
        
        print(f"Found {len(messages)} unread messages.")
        return messages

    def save_to_inbox(self, item):
        # ... (method unchanged)
        content_str = str(item)
        content_hash = hashlib.md5(content_str.encode()).hexdigest()

        if content_hash in self.seen_ids:
            print(f"Skipping duplicate item: {content_str[:70]}...")
            return

        timestamp = datetime.now()
        filename = f"LINKEDIN_{item['type'].upper()}_{timestamp.strftime('%Y%m%d%H%M%S')}_{content_hash[:8]}.md"
        filepath = os.path.join(self.vault_path, filename)

        body = ""
        if item['type'] == 'notification':
            title = f"New LinkedIn Notification: {item['content'][:40]}..."
            body = item['content']
        elif item['type'] == 'message':
            title = f"New LinkedIn Message from {item['sender']}"
            body = f"**From:** {item['sender']}\n\n**Message Snippet:**\n{item['snippet']}"

        frontmatter = f"""---
title: "{title}"
source: linkedin
type: {item['type']}
status: new
timestamp: {timestamp.isoformat()}
hash: {content_hash}
---
"""
        
        content = frontmatter + "\n" + body
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.seen_ids.add(content_hash)
        print(f"Saved new item to {filepath}")

    async def run(self):
        # ... (method unchanged)
        print("Starting LinkedIn Watcher...")
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(storage_state=self.session_path)
            page = await context.new_page()
            
            notifications = await self.check_notifications(page)
            for notification in notifications:
                self.save_to_inbox(notification)

            messages = await self.check_messages(page)
            for message in messages:
                self.save_to_inbox(message)
            
            await browser.close()
        
        self._update_cache()
        print("LinkedIn Watcher finished.")

async def main():
    """
    Main function to run the LinkedIn Watcher.
    """
    try:
        watcher = LinkedInWatcher()
        await watcher.run()
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
