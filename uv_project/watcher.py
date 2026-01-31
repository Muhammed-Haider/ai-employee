import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

# Import your Agent Skills
from agent_skills.file_skills.process_file import process_file_with_claude
from agent_skills.file_skills.write_vault import write_dashboard_entry




class InboxHandler(FileSystemEventHandler):
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.inbox = self.vault_path / "Inbox"
        self.inbox.mkdir(exist_ok=True)
    
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith((".tmp", ".swp")):
            return

        # Analyze FIRST
        result = process_file_with_claude(event.src_path)
        
        # Move based on decision
        if result['destination'] == 'Needs_Action':
            dest = self.vault_path / "Needs_Action" / Path(event.src_path).name
        else:
            dest = self.vault_path / "Done" / Path(event.src_path).name
        
        dest.parent.mkdir(exist_ok=True)
        
        # Remove existing file if it exists
        if dest.exists():
            dest.unlink()
        
        Path(event.src_path).rename(dest)
        
        # Log it
        write_dashboard_entry(self.vault_path, 
            f"[{result['category']}] {dest.name}: {result['summary']} (Priority: {result['priority']})")
        
        # Print to terminal
        print(f"New file detected: {event.src_path} -> moved to {dest}")
        print(f"  Category: {result['category']}, Priority: {result['priority']}, Action Needed: {result['action_needed']}")


def watch_inbox(vault_path):
    handler = InboxHandler(vault_path)
    observer = Observer()
    observer.schedule(handler, str(handler.inbox), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    BASE_DIR = Path(__file__).parent
    VAULT_PATH = BASE_DIR.parent / "AI_Employee_Vault"
    watch_inbox(VAULT_PATH)
