from pathlib import Path

def write_dashboard_entry(vault_path: Path, text: str):
    dashboard = vault_path / "Dashboard.md"
    with open(dashboard, "a", encoding="utf-8") as f:
        f.write(f"- {text}\n")
