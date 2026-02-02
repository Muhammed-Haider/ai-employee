import time
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

VAULT = Path("../AI_Employee_Vault")
INBOX = VAULT / "Inbox"

class GmailWatcher:
    def __init__(self, creds_path):
        self.creds = Credentials.from_authorized_user_file(creds_path)
        self.service = build("gmail", "v1", credentials=self.creds)

    def poll(self):
        res = self.service.users().messages().list(
            userId="me", q="is:unread", maxResults=3
        ).execute()
        return res.get("messages", [])

    def run(self):
        INBOX.mkdir(exist_ok=True)
        print("Watcher started. Checking for unread emails every 120 seconds...")
        while True:
            messages = self.poll()
            if not messages:
                print("No new unread emails found.")
            
            for msg in messages:
                print(f"New email found! ID: {msg['id']}")
                data = self.service.users().messages().get(
                    userId="me", id=msg["id"]
                ).execute()

                headers = {
                    h["name"]: h["value"]
                    for h in data["payload"]["headers"]
                }

                content = f"""---
type: email
id: {msg['id']}
from: {headers.get('From')}
subject: {headers.get('Subject')}
status: new
---

{data.get('snippet')}
"""
                path = INBOX / f"EMAIL_{msg['id']}.md"
                path.write_text(content, encoding="utf-8")
                print(f"Saved email to {path.name}")
                self.service.users().messages().modify(userId='me', id=msg['id'], body={'removeLabelIds': ['UNREAD']}).execute()
                print(f"Marked email {msg['id']} as read.")

            time.sleep(120)

if __name__ == "__main__":
    GmailWatcher("gmail_token.json").run()
