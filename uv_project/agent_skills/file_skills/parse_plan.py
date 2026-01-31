import re

def parse_plan(plan_text: str):
    """
    Parses a Plan.md file to extract email details.
    Expected format:
    ---
    status: approved
    recipient: example@test.com
    subject: Re: Hello
    ---
    BODY STARTS HERE
    """
    # Extract metadata using regex
    meta_match = re.search(r'---\s*(.*?)\s*---', plan_text, re.DOTALL)
    if not meta_match:
        return None

    metadata = {}
    for line in meta_match.group(1).split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            metadata[key.strip().lower()] = val.strip()

    # Extract body (everything after the second ---)
    parts = plan_text.split('---')
    body = parts[2].strip() if len(parts) > 2 else ""

    return {
        "recipient": metadata.get("recipient"),
        "subject": metadata.get("subject"),
        "body": body,
        "status": metadata.get("status")
    }
