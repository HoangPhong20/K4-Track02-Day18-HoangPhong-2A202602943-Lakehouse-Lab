"""Render logs with Windows System.Drawing without changing execution policy."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
if __name__ == "__main__":
    commands = (ROOT / "scripts" / "render_evidence.ps1").read_text(encoding="utf-8")
    subprocess.run(["powershell", "-NoProfile", "-Command", commands], cwd=ROOT, check=True)
