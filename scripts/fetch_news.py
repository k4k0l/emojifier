"""Fetch current events using OpenAI's Deep Research API and store as JSON."""
from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict, List

from openai import OpenAI


client = OpenAI()


def fetch_news() -> List[Dict[str, Any]]:
    """Use the Deep Research API to retrieve today's news.

    The model is instructed to return a JSON object with an ``items`` list.
    Each item should contain ``id``, ``title``, ``date``, ``content`` and
    ``sources``.
    """

    response = client.responses.create(
        model="gpt-4.1",
        input=(
            "Use web browsing to gather today's top world news. "
            "Return a JSON object with a key 'items' containing a list of "
            "objects with fields: id (slug), title, date, content, sources."),
        extra_body={
            "reasoning": {"effort": "medium"},
            "data_sources": [{"type": "web"}],
        },
    )

    try:
        payload = json.loads(response.output_text)
    except Exception:
        raise RuntimeError("Model response was not valid JSON")
    return payload.get("items", [])


def main() -> None:
    items = fetch_news()
    os.makedirs("news", exist_ok=True)
    for item in items:
        item.setdefault("date", datetime.utcnow().isoformat())
        path = os.path.join("news", f"{item['id']}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(item, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
