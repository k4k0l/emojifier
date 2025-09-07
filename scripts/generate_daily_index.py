"""Generate a daily index file referencing news items."""
from __future__ import annotations

import json
import glob
import os
from datetime import datetime


def main() -> None:
    today = datetime.utcnow().strftime("%Y-%m-%d")
    news_ids = []
    for path in glob.glob(os.path.join("news", "*.json")):
        news_ids.append(os.path.splitext(os.path.basename(path))[0])
    data = {"date": today, "news": news_ids}
    os.makedirs("daily", exist_ok=True)
    daily_path = os.path.join("daily", f"{today}.json")
    with open(daily_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    latest_path = os.path.join("daily", "latest.json")
    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
