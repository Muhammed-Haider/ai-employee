import subprocess
import os
import tempfile
from pathlib import Path
import re

def plan_email(email_md: str) -> str:
    prompt = f"""
You are an AI employee.
Read this email and create a Plan.md. The plan should be formatted as a markdown document with the following sections:
- Intent: [One sentence describing the primary goal based on the email]
- Proposed Action: [Numbered list of concrete steps the AI Employee would take]
- Draft Response: [A draft email or message to the sender, with placeholders for information not yet available]
- status: awaiting_approval

Output ONLY the markdown content for the Plan.md, ensuring it adheres strictly to the requested format and includes no conversational text or explanations.

EMAIL:
{email_md}
"""
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as tmp:
        tmp.write(prompt)
        tmp_path = tmp.name
    
    try:
        result = subprocess.run(
            ['cmd', '/c', 'ccr', 'code', '--print', tmp_path],
            capture_output=True,
            text=True,
            shell=False,
            stdin=subprocess.DEVNULL
        )
        full_output = result.stdout.strip()

        # Try to find content starting from "1. **Intent**" or "Intent:"
        plan_start_match = re.search(r'(^1\.\s*\*\*Intent\*\*|^\s*Intent:)', full_output, re.MULTILINE | re.IGNORECASE)
        if plan_start_match:
            # Extract from that point onwards
            extracted_plan = full_output[plan_start_match.start():].strip()
            # Then, try to find the "status: awaiting_approval" at the end of this extracted plan
            status_match = re.search(r'^status:\s*awaiting_approval.*', extracted_plan, re.MULTILINE | re.IGNORECASE)
            if status_match:
                # If status is found, return the extracted plan up to and including the status line
                return extracted_plan[:status_match.end()].strip()
            else:
                # If status not found, return the whole extracted block and let brain_loop decide
                return extracted_plan
        
        # Fallback: if no clear plan start is found, return the entire output
        return full_output

    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
