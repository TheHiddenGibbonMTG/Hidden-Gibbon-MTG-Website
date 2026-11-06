"""Sync public Google Drive historical cards without Google account credentials.

Google's public embedded folder listing is used instead of gdown.download_folder,
which caps discovery at 50 items in gdown 5.x.
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

import gdown
import requests
from bs4 import BeautifulSoup

FOLDER_ID = "1qw1OYpqzH7h8SlP6-0oSUhJ8seHg-WKJ"
DEST = Path("historical-cards")
MANIFEST = Path("historical-cards.json")
EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
MIN_EXPECTED = 117  # User confirmed this many public cards as of Nov 2026.
DEST.mkdir(exist_ok=True)

url = "https://drive.google.com/embeddedfolderview?id=" + FOLDER_ID
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")
found = {}
for link in soup.find_all("a", href=True):
    match = re.search(r"drive\\.google\\.com/file/d/([\\w-]{25,})/view", link["href"])
    if not match:
        continue
    name = link.get_text(" ", strip=True).strip()
    if not name or Path(name).suffix.lower() not in EXTENSIONS:
        continue
    # Never allow names from a public HTML listing to escape the image folder.
    name = Path(name.replace("\\", "/")).name
    if name in found and found[name] != match.group(1):
        raise RuntimeError("Duplicate file name in public Drive folder: " + name)
    found[name] = match.group(1)

print(f"Discovered {len(found)} image files in public Google Drive folder.", flush=True)
if len(found) < MIN_EXPECTED:
    raise RuntimeError(
        f"Only discovered {len(found)} images; expected at least {MIN_EXPECTED}. "
        "Refusing to publish an incomplete gallery."
    )

failed = []
for n, (name, file_id) in enumerate(sorted(found.items(), key=lambda item: item[0].casefold()), 1):
    destination = DEST / name
    if destination.is_file() and destination.stat().st_size > 0:
        continue
    try:
        result = gdown.download(
            id=file_id, output=str(destination), quiet=True, fuzzy=True,
        )
        if not result or not destination.is_file() or destination.stat().st_size == 0:
            raise RuntimeError("Empty or missing download")
    except Exception as exc:
        failed.append(f"{name}: {exc}")
    if n % 20 == 0:
        print(f"Processed {n}/{len(found)}", flush=True)
if failed:
    raise RuntimeError("Failed to download " + str(len(failed)) + " cards: " + "; ".join(failed[:10]))

cards = [
    {"name": Path(name).stem.replace("_", " ").replace("-", " "),
     "url": "historical-cards/" + quote(name)}
    for name in sorted(found, key=str.casefold)
]
MANIFEST.write_text(json.dumps({"cards": cards}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Published manifest for {len(cards)} historical cards.", flush=True)
