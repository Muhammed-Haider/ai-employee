import time
import logging
from pathlib import Path
import yaml
from agent_skills.ai_skills.draft_email import draft_email_from_plan

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class VaultWorker:
    """
    A worker that watches for approved plans in the vault and executes them.
    """
    def __init__(self, vault_path="../AI_Employee_Vault"):
        self.vault_path = Path(vault_path)
        self.needs_action_path = self.vault_path / "Needs_Action"
        self.done_path = self.vault_path / "Done"
        
        self.dispatcher = {
            "draft_email": self.handle_draft_email
        }

        # Ensure directories exist
        self.needs_action_path.mkdir(exist_ok=True)
        self.done_path.mkdir(exist_ok=True)

        logging.info("Vault Worker initialized.")
        logging.info(f"Watching: {self.needs_action_path}")

    def find_approved_plans(self):
        """
        Finds plan files in the Needs_Action directory that have been approved.
        """
        approved_plans = []
        for plan_path in self.needs_action_path.glob("PLAN_*.md"):
            try:
                with open(plan_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # A simple check for the status in the frontmatter
                    if "status: approved" in content.split("---")[1]:
                        approved_plans.append(plan_path)
            except Exception as e:
                logging.error(f"Error reading or parsing {plan_path}: {e}")
        return approved_plans

    def parse_plan(self, plan_path):
        """
        Parses a plan file to find the specified action.
        """
        try:
            with open(plan_path, 'r', encoding='utf-8') as f:
                content = f.read()
                for line in content.splitlines():
                    if line.startswith("Action:"):
                        action = line.split("Action:")[1].strip()
                        return action, content
        except Exception as e:
            logging.error(f"Error parsing plan {plan_path}: {e}")
        return None, None

    def handle_draft_email(self, plan_content):
        """
        Handles the draft_email action by calling the appropriate skill.
        """
        logging.info("Handling action: draft_email")
        return draft_email_from_plan(plan_content)

    def archive_completed_item(self, plan_path):
        """
        Moves the completed plan and its source file to the Done directory.
        """
        try:
            # Derive source file name from plan file name
            source_filename = plan_path.name.replace("PLAN_", "")
            source_path = self.needs_action_path / source_filename

            # Move plan file
            plan_path.rename(self.done_path / plan_path.name)
            logging.info(f"Archived plan: {plan_path.name}")

            # Move source file if it exists
            if source_path.exists():
                source_path.rename(self.done_path / source_path.name)
                logging.info(f"Archived source: {source_path.name}")
            else:
                logging.warning(f"Source file not found for {plan_path.name}, only archived plan.")

        except Exception as e:
            logging.error(f"Error during archiving of {plan_path.name}: {e}")

    def run(self):
        """
        The main loop for the worker.
        """
        logging.info("Vault Worker started. Press Ctrl+C to stop.")
        while True:
            logging.info("Checking for approved plans...")
            approved_plans = self.find_approved_plans()

            if not approved_plans:
                logging.info("No approved plans found.")
            else:
                logging.info(f"Found {len(approved_plans)} approved plans.")
                for plan_path in approved_plans:
                    logging.info(f"Processing {plan_path.name}")
                    action, content = self.parse_plan(plan_path)

                    if action:
                        logging.info(f"Action found: {action}")
                        handler = self.dispatcher.get(action)
                        if handler:
                            success = handler(content)
                            if success:
                                logging.info(f"Successfully executed action: {action}")
                                self.archive_completed_item(plan_path)
                            else:
                                logging.error(f"Failed to execute action: {action}")
                        else:
                            logging.warning(f"No handler found for action: {action}")
                    else:
                        logging.warning(f"No action found in {plan_path.name}")

            time.sleep(30) # Wait for 30 seconds before the next check

if __name__ == "__main__":
    try:
        worker = VaultWorker()
        worker.run()
    except KeyboardInterrupt:
        logging.info("\nVault Worker stopped by user.")