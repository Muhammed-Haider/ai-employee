import time
import os
import re
import shutil
from pathlib import Path
from datetime import datetime
from agent_skills.file_skills.read_md import read_md
from agent_skills.file_skills.write_md import write_md
from agent_skills.ai_skills.send_email_direct import send_email_direct
from agent_skills.ai_skills.generate_x_post import generate_x_post
from agent_skills.browser_skills.post_to_x import post_to_x

VAULT = Path("../AI_Employee_Vault")
INBOX = VAULT / "Inbox"
DRAFTS = VAULT / "Drafts"
ARCHIVE = VAULT / "Archive"
EMAIL_FILE = VAULT / "send_email.md"

def parse_metadata(content: str):
    meta_match = re.search(r'---\s*(.*?)\s*---', content, re.DOTALL)
    if not meta_match:
        return {}
    metadata = {}
    for line in meta_match.group(1).split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            metadata[key.strip().lower()] = val.strip()
    return metadata

def process_inbox():
    """Checks Inbox for new items to turn into X drafts."""
    for file in INBOX.glob("*.md"):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Processing Inbox item: {file.name}")
        content = read_md(file)
        
        # Generate the 50-char post
        post_text = generate_x_post(content)
        
        draft_content = f"""---
status: pending
type: x_post
original_file: {file.name}
---
{post_text}
"""
        draft_name = f"DRAFT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        write_md(DRAFTS / draft_name, draft_content)
        
        # Move original to Archive
        shutil.move(file, ARCHIVE / file.name)
        print(f"SUCCESS: Draft created: {draft_name}")

def process_drafts():
    """Checks Drafts for approved X posts."""
    for file in DRAFTS.glob("*.md"):
        content = read_md(file)
        metadata = parse_metadata(content)
        
        if metadata.get("status") == "approved":
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Detected approved X post in {file.name}")
            
            # Extract post text (after the second ---)
            parts = content.split('---')
            post_text = parts[2].strip() if len(parts) > 2 else ""
            
            if post_text:
                result = post_to_x(post_text)
                if result.get("success"):
                    print(f"SUCCESS: Posted to X: {post_text}")
                    # Move to Archive with result
                    final_content = content + f"\n\n--- POSTED ---\nURL: {result.get('url', 'N/A')}\nTime: {result.get('timestamp')}"
                    write_md(file, final_content)
                    shutil.move(file, ARCHIVE / file.name)
                else:
                    print(f"FAILED: Could not post to X: {result.get('error')}")
                    new_content = content.replace("status: approved", "status: failed")
                    write_md(file, new_content)

def process_emails():
    """Legacy support for the send_email.md file."""
    if not EMAIL_FILE.exists():
        return
    
    content = read_md(EMAIL_FILE)
    metadata = parse_metadata(content)
    
    if metadata.get("status") == "send":
        recipient = metadata.get("recipient")
        subject = metadata.get("subject")
        parts = content.split('---')
        body = parts[2].strip() if len(parts) > 2 else ""
        
        if recipient and body:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Sending email to {recipient}")
            success = send_email_direct(recipient, subject or "(No Subject)", body)
            if success:
                write_md(EMAIL_FILE, content.replace("status: send", "status: sent"))
            else:
                write_md(EMAIL_FILE, content.replace("status: send", "status: failed"))

def run_worker():
    print(f"Vault Worker started. Monitoring {VAULT.absolute()}...", flush=True)
    while True:
        try:
            process_inbox()
            process_drafts()
            process_emails()
        except Exception as e:
            print(f"ERROR: Worker encountered an error: {e}")
        time.sleep(10)

if __name__ == "__main__":
    run_worker()
