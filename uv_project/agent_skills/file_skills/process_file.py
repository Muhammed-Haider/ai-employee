import subprocess
import json
from pathlib import Path
import time

def process_file_with_claude(file_path: str) -> dict:
    '''Agent Skill: Analyze file and decide action'''
    
    MAX_RETRIES = 5
    RETRY_DELAY = 1 # seconds

    content = ""
    for i in range(MAX_RETRIES):
        try:
            content = Path(file_path).read_text(encoding='utf-8')[:2000]
            if content.strip(): # If content is not empty, we succeeded
                break
        except (PermissionError, FileNotFoundError, OSError) as e:
            # File might be locked or not fully created yet
            print(f"DEBUG: File read attempt {i+1} failed for {file_path}: {e}")
        except UnicodeDecodeError:
            try:
                content = Path(file_path).read_text(encoding='utf-16')[:2000]
                if content.strip():
                    break
            except Exception as e:
                print(f"DEBUG: UnicodeDecodeError fallback attempt {i+1} failed for {file_path}: {e}")
        
        time.sleep(RETRY_DELAY) # Wait before retrying
    
    if not content.strip():
        print(f"ERROR: Could not read content from {file_path} after {MAX_RETRIES} attempts.")
        # Fallback for process_file_with_claude if content remains empty
        return {
            "category": "Note",
            "summary": "Unable to read file content after multiple attempts",
            "action_needed": False,
            "priority": "low",
            "destination": "Done"
        }
    
    print(f"DEBUG: Content passed to Claude: [{content}]")
    
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
```
{content}
```'''
    
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
    
    print(f"DEBUG: Raw CCR output length: {len(output)}")
    
    # Try to find JSON block within markdown fences
    json_match = re.search(r'```json\s*(.*?)\s*```', output, re.DOTALL)
    if json_match:
        output = json_match.group(1)
    else:
        # Fallback: try to find just the JSON object by finding the first '{' and last '}'
        start_brace = output.find('{')
        end_brace = output.rfind('}')
        if start_brace != -1 and end_brace != -1 and end_brace > start_brace:
            output = output[start_brace : end_brace + 1]
            
    print(f"DEBUG: Cleaned output for parsing: {output}")
    try:
        return json.loads(output)
    except json.JSONDecodeError as e:
        print(f"JSON Parsing Error: {e}")
        # Final fallback attempt: strip conversational preamble
        if '{' in output and '}' in output:
             start = output.find('{')
             end = output.rfind('}') + 1
             try:
                 return json.loads(output[start:end])
             except:
                 pass
        raise e
