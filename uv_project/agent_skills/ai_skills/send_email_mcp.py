import subprocess
import json
import os
import tempfile
import re
from pathlib import Path

def send_email_mcp(recipient: str, subject: str, message: str) -> bool:
    '''Agent Skill: Send email using CCR (Matching process_file.py working pattern)'''
    
    prompt = f'''You must respond ONLY with valid JSON. Do not ask questions. Do not add explanations. Just analyze and output JSON.

Task: Use the Gmail MCP tool to send an email with the following details:
Recipient: {recipient}
Subject: {subject}
Body:
{message}

After sending the email, respond ONLY with this JSON structure:
{{
  "success": true,
  "details": "Summary of what happened"
}}'''
    
    # Create a temporary file for the prompt to avoid shell arg limits/issues
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as tmp:
        tmp.write(prompt)
        tmp_path = tmp.name
    
    try:
        # Use ccr code command with --print and the temp file path
        # This matches the working process_file.py configuration exactly
        result = subprocess.run(
            ['cmd', '/c', 'ccr', 'code', '--print', tmp_path], 
            capture_output=True, 
            text=True, 
            shell=False,
            stdin=subprocess.DEVNULL,
            timeout=300
        )
    finally:
        # cleanup
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
    
    # Debug: print what we got
    print(f"CCR stdout: {result.stdout}", flush=True)
    print(f"CCR stderr: {result.stderr}", flush=True)
    print(f"CCR return code: {result.returncode}", flush=True)
    
    if result.returncode != 0 or not result.stdout.strip():
        print(f"Error: CCR command failed or returned empty output", flush=True)
        return False
    
    # Clean up output and parse JSON
    output = result.stdout.strip()
    
    # Try to find JSON block
    json_match = re.search(r'```json\s*(.*?)\s*```', output, re.DOTALL)
    if json_match:
        output = json_match.group(1)
    else:
        # Fallback: try to find just the JSON object start/end
        json_obj_match = re.search(r'(\{.*\})', output, re.DOTALL)
        if json_obj_match:
            output = json_obj_match.group(1)
            
    try:
        res_json = json.loads(output)
        return res_json.get("success", False)
    except Exception as e:
        print(f"Error parsing JSON from CCR: {e}", flush=True)
        # Fallback check for "success" in text if JSON parsing fails
        if '"success": true' in output.lower() or 'email sent' in output.lower():
            return True
        return False
