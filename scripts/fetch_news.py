"""Fetch current events using OpenAI's Deep Research API and store as JSON."""
from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict, List

from openai import OpenAI


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def fetch_news() -> List[Dict[str, Any]]:
    """Use the Deep Research API to retrieve today's news.

    The model is instructed to return a JSON object with an ``items`` list.
    Each item should contain ``id``, ``title``, ``date``, ``content`` and
    ``sources``.
    """

    system_prompt = (
        "You are a researcher. Gather today's top news "
        "and return a JSON object: items list with fields "
        "id (slug), title, date, content, sources (list of URLs)."
    )
    user_prompt = (
        "Please gather current events and format response in JSON."
    )

    response = client.responses.create(
        model="o4-mini-deep-research-2025-06-26",
        input=[
            {"role": "developer", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        tools=[{"type": "web_search_preview"}],
        reasoning={"summary": "auto"}
    )

    output_text = response.output[-1].content[0].text
    try:
        payload = json.loads(output_text)
    except Exception as e:
        raise RuntimeError(f"Model response was not valid JSON: {e}")

    return payload.get("items", [])


def main() -> None:
    items = fetch_news()
    os.makedirs("news", exist_ok=True)
    for item in items:
        item.setdefault("date", datetime.utcnow().isoformat())
        fname = f"{item['id']}.json"
        path = os.path.join("news", fname)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(item, f, ensure_ascii=False, indent=2)
        print("Saved", path)


if __name__ == "__main__":
    main()
