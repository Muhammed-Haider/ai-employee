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
        for item_path in NEEDS_ACTION.iterdir():
            if not item_path.is_file() or item_path.suffix != ".md" or item_path.name.startswith("PLAN_"):
                continue

            # Check if a plan already exists for this item
            plan_path = NEEDS_ACTION / f"PLAN_{item_path.stem}.md" # Use stem to be more general
            if plan_path.exists():
                continue

            print(f"Processing new item for planning: {item_path.name}")
            text = read_md(item_path)
            
            print("Requesting plan from Claude...")
            plan = plan_email(text) # Assuming plan_email can handle general text
            
            write_md(plan_path, plan)
            print(f"Plan saved to {plan_path.name}")

            # Optionally, mark the original item as processed or move it to a 'planned' subfolder
            # For now, we'll just create the plan.

        time.sleep(60)

if __name__ == "__main__":
    run_brain()
