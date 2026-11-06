"""Synchronize publicly shared historical Commander card images without Google credentials."""
import json
import re
from pathlib import Path
import gdown

FOLDER_URL = "https://drive.google.com/drive/folders/1qw1OYpqzH7h8SlP6-0oSUhJ8seHg-WKJ"
DEST = Path("historical-cards")
MANIFEST = Path("historical-cards.json")
EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
DEST.mkdir(exist_ok=True)

# gdown can enumerate public folders without an OAuth token, subject to Google's limits.
files = gdown.download_folder(url=FOLDER_URL, output=str(DEST), quiet=True, remaining_ok=True)
if files is None:
    raise RuntimeError("Public Google Drive folder could not be read; keeping existing gallery.")

cards = []
for p in sorted(DEST.iterdir(), key=lambda p: p.name.casefold()):
    if p.is_file() and p.suffix.lower() in EXTENSIONS:
        cards.append({"name": p.stem.replace("_", " ").replace("-", " "), "url": "historical-cards/" + p.name})
if not cards:
    raise RuntimeError("No supported images retrieved; keeping existing gallery.")
MANIFEST.write_text(json.dumps({"cards": cards}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Prepared {len(cards)} historical cards.")
