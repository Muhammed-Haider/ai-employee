import subprocess
import json
from pathlib import Path

def process_file_with_claude(file_path: str) -> dict:
    '''Agent Skill: Analyze file and decide action'''
    
    content = Path(file_path).read_text(encoding='utf-8')[:2000]
    
    prompt = f'''You must respond ONLY with valid JSON. Do not ask questions. Do not add explanations. Just analyze and output JSON.

Analyze this file and respond with this exact JSON structure:
{{
  "category": "Report|Email|Task|Meeting|Note",
  "summary": "one sentence summary",
  "action_needed": true or false,
  "priority": "high|medium|low",
  "destination": "Needs_Action" or "Done"
}}

File content:
{content}'''
    
    import tempfile
    import os

    # Create a temporary file for the prompt to avoid shell arg limits/issues
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as tmp:
        tmp.write(prompt)
        tmp_path = tmp.name
    
    try:
        # Use ccr code command with --print and the temp file path
        # METHOD: cmd /c + shell=False + DEVNULL stdin prevents hanging
        # This matches the working debug_ccr.py configuration exactly
        result = subprocess.run(
            ['cmd', '/c', 'ccr', 'code', '--print', tmp_path], 
            capture_output=True, 
            text=True, 
            shell=False,
            stdin=subprocess.DEVNULL
        )
    finally:
        # cleanup
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
    
    # Debug: print what we got
    print(f"CCR stdout: {result.stdout}")
    print(f"CCR stderr: {result.stderr}")
    print(f"CCR return code: {result.returncode}")
    
    if result.returncode != 0 or not result.stdout.strip():
        print(f"Error: CCR command failed or returned empty output")
        # Fallback: return a default response for testing
        return {
            "category": "Note",
            "summary": "Unable to analyze - CCR not responding",
            "action_needed": True,
            "priority": "medium",
            "destination": "Needs_Action"
        }
    
    import re
    
    # Clean up markdown formatting if present
    output = result.stdout.strip()
    
    # Try to find JSON block within markdown fences
    json_match = re.search(r'```json\s*(.*?)\s*```', output, re.DOTALL)
    if json_match:
        output = json_match.group(1)
    else:
        # Fallback: try to find just the JSON object start/end
        json_obj_match = re.search(r'(\{.*\})', output, re.DOTALL)
        if json_obj_match:
            output = json_obj_match.group(1)
            
    return json.loads(output)
