import os
import json
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _write_status(payload: dict) -> None:
    with open("status.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def main() -> None:
    if not os.path.exists("pending.txt"):
        raise RuntimeError("Brak pliku pending.txt \u2014 nie wys\u0142ano zapytania")

    with open("pending.txt", "r", encoding="utf-8") as f:
        response_id = f.read().strip()

    print(f"\ud83d\udd04 Sprawdzanie statusu dla ID: {response_id}")
    result = client.responses.retrieve(response_id)
    print(f"\ud83d\udcca Status: {result.status}")

    if result.status == "in_progress":
        _write_status(
            {
                "status": "in_progress",
                "response_id": response_id,
                "updated_at": datetime.utcnow().isoformat(),
            }
        )
        print("\u231b Odpowied\u017a jeszcze si\u0119 generuje. Uruchom ponownie p\u00f3\u017aniej.")
        raise SystemExit(1)

    if result.status != "completed":
        _write_status(
            {
                "status": "failed",
                "response_id": response_id,
                "updated_at": datetime.utcnow().isoformat(),
                "error": result.status,
            }
        )
        raise RuntimeError(f"\u26d4 \u017badanie zako\u0144czone niepowodzeniem: {result.status}")

    output_text = result.output[-1].content[0].text

    try:
        payload = json.loads(output_text)
    except Exception as e:  # pragma: no cover - defensive
        _write_status(
            {
                "status": "failed",
                "response_id": response_id,
                "updated_at": datetime.utcnow().isoformat(),
                "error": "invalid_json",
            }
        )
        raise RuntimeError(f"\u274c Niepoprawny JSON: {e}")

    items = payload.get("items", [])
    if not items:
        _write_status(
            {
                "status": "failed",
                "response_id": response_id,
                "updated_at": datetime.utcnow().isoformat(),
                "error": "empty_items",
            }
        )
        raise RuntimeError("Brak element\u00f3w w `items`")

    os.makedirs("news", exist_ok=True)
    for item in items:
        item.setdefault("date", datetime.utcnow().isoformat())
        fname = f"{item['id']}.json"
        path = os.path.join("news", fname)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(item, f, ensure_ascii=False, indent=2)
        print(f"\u2705 Zapisano news: {fname}")

    os.remove("pending.txt")
    print("\ud83e\uddf9 Usuni\u0119to pending.txt \u2014 zako\u0144czono cykl.")

    _write_status(
        {
            "status": "completed",
            "response_id": response_id,
            "updated_at": datetime.utcnow().isoformat(),
            "items": [item["id"] for item in items],
        }
    )
    print("\ud83d\udcc4 Zaktualizowano status.json")


if __name__ == "__main__":
    main()
