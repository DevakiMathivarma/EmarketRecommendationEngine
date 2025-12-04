import json, re, shutil
from pathlib import Path

# ---------------------------------------------------------
# PUT YOUR JSON FILE PATH HERE
# Example:
# json_path = r"C:\Users\You\Desktop\products.json"
# ---------------------------------------------------------
json_path = "home_beauty.json"   # ← PUT YOUR JSON FILE PATH HERE
# ---------------------------------------------------------

THUMB_RE = re.compile(r"^thumbnail(\d+)$", re.IGNORECASE)

def new_thumb_path(old_path, index):
    """
    Keep the same folder and append /thumbnails/image{index}_thumb.jpg
    """
    if not isinstance(old_path, str):
        return None

    old_path = old_path.strip()

    if "/" in old_path:
        folder = old_path.rsplit("/", 1)[0]          # eg: /static/core/ecom/fashion_accessories
    else:
        folder = ""  # unexpected case

    return f"{folder}/thumbnails/image{index}_thumb.jpg"


def process_fields(fields):
    updated = 0
    for key, value in fields.items():
        m = THUMB_RE.match(key)
        if m:
            idx = int(m.group(1))
            new_val = new_thumb_path(value, idx)
            if new_val:
                fields[key] = new_val
                updated += 1
    return updated


# ---------------------------------------------------------
# Load JSON
# ---------------------------------------------------------
json_file = Path(json_path)

if not json_file.exists():
    print("❌ ERROR: JSON file not found!")
    print("Path:", json_path)
    exit()

# Backup file
shutil.copy2(json_file, json_file.with_suffix(".bak"))
print("✔ Backup created:", json_file.with_suffix(".bak"))

data = json.loads(json_file.read_text(encoding="utf-8"))

total_updated = 0

# Handle list of objects OR single object
if isinstance(data, list):
    for item in data:
        fields = item.get("fields")
        if isinstance(fields, dict):
            total_updated += process_fields(fields)

elif isinstance(data, dict):
    fields = data.get("fields")
    if isinstance(fields, dict):
        total_updated += process_fields(fields)

# Save back
json_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

print(f"✔ Done! Updated {total_updated} thumbnail values.")
