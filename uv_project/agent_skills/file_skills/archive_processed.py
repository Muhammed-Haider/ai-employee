import shutil
from pathlib import Path

def archive_processed(email_path: Path, plan_path: Path, done_dir: Path):
    """
    Moves the original email and the generated plan to the Done directory.
    """
    done_dir.mkdir(exist_ok=True)
    
    if email_path.exists():
        shutil.move(str(email_path), str(done_dir / email_path.name))
        
    if plan_path.exists():
        shutil.move(str(plan_path), str(done_dir / plan_path.name))

    print(f"Archived {email_path.name} and {plan_path.name} to {done_dir}")
