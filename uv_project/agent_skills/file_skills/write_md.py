from pathlib import Path

def write_md(path: Path, content: str) -> None:
    """Writes content to a markdown file."""
    path.write_text(content, encoding="utf-8")
