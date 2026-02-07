import time
from pathlib import Path
import re

DRAFTS_PATH = Path("../AI_Employee_Vault/Drafts")

def draft_email_from_plan(plan_content: str) -> bool:
    """
    Parses a plan's content to generate a draft email as a markdown file.

    Args:
        plan_content: The full string content of the plan file.

    Returns:
        True if the draft was created successfully, False otherwise.
    """
    try:
        DRAFTS_PATH.mkdir(exist_ok=True)

        # Simple parsing logic. Assumes a structured plan.
        to_match = re.search(r"To:\s*(.*)", plan_content)
        subject_match = re.search(r"Subject:\s*(.*)", plan_content)
        
        # Find the body after the '---' separator
        body_parts = plan_content.split("---", 1)
        body = body_parts[1].strip() if len(body_parts) > 1 else "No body content found in plan."

        if not to_match or not subject_match:
            print("ERROR: Could not parse To/Subject from plan.")
            return False

        recipient = to_match.group(1).strip()
        subject = subject_match.group(1).strip()
        
        timestamp = time.strftime("%Y%m%d%H%M%S")
        draft_filename = f"DRAFT_EMAIL_{timestamp}.md"
        draft_path = DRAFTS_PATH / draft_filename

        draft_frontmatter = f"""---
status: draft
recipient: {recipient}
subject: "{subject}"
---

"""
        draft_content = draft_frontmatter + body

        with open(draft_path, 'w', encoding='utf-8') as f:
            f.write(draft_content)
        
        print(f"Successfully created email draft: {draft_path}")
        return True

    except Exception as e:
        print(f"ERROR: Failed to create email draft: {e}")
        return False

if __name__ == '__main__':
    # Standalone test
    test_plan = """
Some planning text...
To: test@example.com
Subject: This is a test subject
---
This is the body of the email.
It can have multiple lines.
"""
    print("Testing draft_email_from_plan...")
    if draft_email_from_plan(test_plan):
        print("SUCCESS")
    else:
        print("FAILED")
