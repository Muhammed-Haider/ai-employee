from pathlib import Path

def read_md(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-16")
        except Exception:
            return path.read_text(encoding="utf-8", errors="replace")
