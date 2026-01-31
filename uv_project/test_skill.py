import sys
from agent_skills.ai_skills.send_email_mcp import send_email_mcp

recipient = "iamhaider072@gmail.com"
subject = "Direct Skill Test"
message = "This is a direct test of the send_email_mcp skill using adopt process_file.py pattern."

print(f"Starting direct test to {recipient}...", flush=True)
try:
    success = send_email_mcp(recipient, subject, message)
    print(f"Result: {'SUCCESS' if success else 'FAILED'}", flush=True)
except Exception as e:
    print(f"CRITICAL ERROR in test loop: {e}", flush=True)
