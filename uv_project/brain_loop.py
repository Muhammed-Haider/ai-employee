import time
from pathlib import Path
from agent_skills.file_skills.read_md import read_md
from agent_skills.file_skills.write_md import write_md
from agent_skills.ai_skills.plan_email import plan_email

VAULT = Path("../AI_Employee_Vault")
NEEDS_ACTION = VAULT / "Needs_Action"

def run_brain():
    print("Brain loop started. Watching for new emails in vault...")
    while True:
        emails = list(NEEDS_ACTION.glob("EMAIL_*.md"))
        for email in emails:
            text = read_md(email)
            if "status: new" not in text:
                continue

            print(f"Processing new email: {email.name}")
            print("Requesting plan from Claude...")
            plan = plan_email(text)
            
            plan_path = NEEDS_ACTION / email.name.replace("EMAIL", "PLAN")
            write_md(plan_path, plan)
            print(f"Plan saved to {plan_path.name}")

            # mark email as planned
            write_md(email, text.replace("status: new", "status: planned"))
            print(f"Marked {email.name} as planned.")

        time.sleep(60)

if __name__ == "__main__":
    run_brain()
