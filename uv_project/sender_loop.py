import time
import os
import re
from pathlib import Path
from agent_skills.file_skills.read_md import read_md
from agent_skills.file_skills.write_md import write_md
from agent_skills.ai_skills.send_email_direct import send_email_direct

VAULT = Path("../AI_Employee_Vault")
EMAIL_FILE = VAULT / "send_email.md"

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
    print(f"Sender loop started. Monitoring {EMAIL_FILE.absolute()} every 10s...", flush=True)
    
    while True:
        if not EMAIL_FILE.exists():
            print(f"DEBUG: {EMAIL_FILE.absolute()} not found. Retrying...", flush=True)
            time.sleep(10)
            continue

        try:
            print(f"DEBUG: Reading {EMAIL_FILE.absolute()}...", flush=True)
            content = read_md(EMAIL_FILE)
            status, recipient, subject, body = parse_email_file(content)
            print(f"DEBUG: Status: {status}, Recipient: {recipient}", flush=True)

            if status == "send" and recipient and body:
                print(f"[{time.strftime('%H:%M:%S')}] Detected request to send email to {recipient}", flush=True)
                
                success = send_email_direct(recipient, subject or "(No Subject)", body)
                
                if success:
                    print(f"SUCCESS: Email sent to {recipient}", flush=True)
                    new_content = content.replace("status: send", "status: sent")
                    write_md(EMAIL_FILE, new_content)
                else:
                    print(f"FAILED: Could not send email to {recipient}", flush=True)
                    new_content = content.replace("status: send", "status: failed")
                    write_md(EMAIL_FILE, new_content)
            
        except Exception as e:
            print(f"ERROR: Loop encountered an error: {e}", flush=True)

        time.sleep(10)

if __name__ == "__main__":
    run_sender()
