import os
import json
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def main() -> None:
    """Send async Deep Research request and store response ID."""
    print("\u23f3 Wysy\u0142anie zapytania do Deep Research...")

    response = client.responses.create(
        model="o3-deep-research-2025-06-26",
        input=[
            {
                "role": "developer",
                "content": (
                    "Zbierz dzisiejsze wydarzenia z Polski, Europy i świata. "
                    "Zwr\u00f3\u0107 dane w formacie JSON z kluczem `items`: lista obiekt\u00f3w zawieraj\u0105cych "
                    "`id` (slug), `title`, `date`, `content`, `sources` (lista link\u00f3w)."
                ),
            },
            {
                "role": "user",
                "content": "Wygeneruj podsumowanie wydarze\u0144 na dzi\u015b w formacie JSON.",
            },
        ],
        tools=[{"type": "web_search_preview"}],
        reasoning={"summary": "auto"},
        stream=False,
        polling={"method": "status_endpoint"},
    )

    response_id = response.id
    print(f"\u2705 Zapytanie wys\u0142ane. ID: {response_id}")

    with open("pending.txt", "w", encoding="utf-8") as f:
        f.write(response_id)
    print("\ud83d\udcdd Zapisano response_id do pending.txt")

    status_payload = {
        "status": "pending",
        "response_id": response_id,
        "updated_at": datetime.utcnow().isoformat(),
    }
    with open("status.json", "w", encoding="utf-8") as f:
        json.dump(status_payload, f, ensure_ascii=False, indent=2)
    print("\ud83d\udcc4 Zaktualizowano status.json")


if __name__ == "__main__":
    main()
