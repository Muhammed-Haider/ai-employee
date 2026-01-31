import subprocess
import os
import tempfile
from pathlib import Path

def plan_email(email_md: str) -> str:
    prompt = f"""
You are an AI employee.

Read this email and create a Plan.md with:
- Intent
- Proposed Action
- Draft Response
- status: awaiting_approval

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
        return result.stdout.strip()
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
