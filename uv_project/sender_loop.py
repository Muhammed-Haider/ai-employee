import time
import os
import re
from pathlib import Path
from agent_skills.file_skills.read_md import read_md
from agent_skills.file_skills.write_md import write_md
from agent_skills.ai_skills.send_email_direct import send_email_direct

VAULT = Path("../AI_Employee_Vault")
DRAFTS_PATH = VAULT / "Drafts"
DONE_PATH = VAULT / "Done"

def parse_email_file(content: str):
    # Extract metadata using regex
    meta_match = re.search(r'---\s*(.*?)\s*---', content, re.DOTALL)
    if not meta_match:
        return None, None, None, None

    metadata = {}
    for line in meta_match.group(1).split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            metadata[key.strip().lower()] = val.strip()

    # Extract body (everything after the second ---)
    parts = content.split('---')
    body = parts[2].strip() if len(parts) > 2 else ""

    return metadata.get("status"), metadata.get("recipient"), metadata.get("subject"), body

def run_sender():
    print(f"Sender loop started. Monitoring {DRAFTS_PATH.absolute()} for approved drafts every 10s...", flush=True)
    
    while True:
        # Ensure directories exist
        DRAFTS_PATH.mkdir(exist_ok=True)
        DONE_PATH.mkdir(exist_ok=True)

        for draft_path in DRAFTS_PATH.glob("DRAFT_EMAIL_*.md"):
            try:
                content = read_md(draft_path)
                status, recipient, subject, body = parse_email_file(content)
                print(f"DEBUG: Processing {draft_path.name} - Status: {status}, Recipient: {recipient}", flush=True)

                if status == "approved" and recipient and body:
                    print(f"[{time.strftime('%H:%M:%S')}] Detected approved draft to send email to {recipient}", flush=True)
                    
                    success = send_email_direct(recipient, subject or "(No Subject)", body)
                    
                    if success:
                        print(f"SUCCESS: Email sent to {recipient}", flush=True)
                        # Move to Done folder
                        draft_path.rename(DONE_PATH / draft_path.name)
                        print(f"Archived draft: {draft_path.name}", flush=True)
                    else:
                        print(f"FAILED: Could not send email to {recipient}", flush=True)
                        # Update status to failed
                        new_content = content.replace("status: approved", "status: failed")
                        write_md(draft_path, new_content)
                
            except Exception as e:
                print(f"ERROR: Loop encountered an error processing {draft_path.name}: {e}", flush=True)

        time.sleep(10)

if __name__ == "__main__":
    run_sender()
