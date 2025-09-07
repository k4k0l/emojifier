"""Deduplicate news items and link related articles."""
from __future__ import annotations

import json
import glob
import os

# Placeholder: marks no duplicates but ensures schema

def main() -> None:
    for path in glob.glob(os.path.join("news", "*.json")):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        data.setdefault("related_to", [])
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
