from pathlib import Path
import shutil

def move_to_needs_action(file_path: str, vault_path: Path):
    src = Path(file_path)
    dest_dir = vault_path / "Needs_Action"
    dest_dir.mkdir(exist_ok=True)

    dest = dest_dir / src.name
    shutil.move(str(src), str(dest))
    return dest
