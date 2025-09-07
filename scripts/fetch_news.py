"""Fetch current events using OpenAI's Deep Research API and store as JSON."""
from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict, List

from openai import OpenAI


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def _query_news(region_prompt: str, max_attempts: int = 5) -> List[Dict[str, Any]]:
    """Execute a single Deep Research query with retry logic."""

    system_prompt = (
        "Jesteś badaczem. Zbierz dzisiejsze najważniejsze wiadomości "
        "i zwróć obiekt JSON: lista items z polami id (slug), "
        "title, date, content, sources (lista URL)."
    )

    for attempt in range(1, max_attempts + 1):
        try:
            response = client.responses.create(
                model="o4-mini-deep-research",
                input=[
                    {"role": "developer", "content": system_prompt},
                    {"role": "user", "content": region_prompt},
                ],
                tools=[{"type": "web_search_preview"}],
                reasoning={"summary": "auto"},
            )

            output_text = response.output[-1].content[0].text
            payload = json.loads(output_text)
            return payload.get("items", [])
        except Exception:
            if attempt == max_attempts:
                raise

    return []


def fetch_news() -> List[Dict[str, Any]]:
    """Retrieve today's news from Poland and worldwide using Deep Research."""

    items: List[Dict[str, Any]] = []

    polish_prompt = (
        "Proszę zbierz aktualne wiadomości z Polski i sformatuj odpowiedź w JSON."
    )
    world_prompt = (
        "Proszę zbierz aktualne wiadomości z całego świata i sformatuj odpowiedź w JSON."
    )

    items.extend(_query_news(polish_prompt))
    items.extend(_query_news(world_prompt))

    return items


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
