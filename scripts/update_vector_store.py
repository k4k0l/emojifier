"""Compute embeddings for news items and update a simple vector store."""
from __future__ import annotations

import glob
import json
import os
from typing import Any, Dict

from openai import OpenAI


client = OpenAI()
STORE_PATH = "vector_store.json"


def load_store() -> Dict[str, Any]:
    if os.path.exists(STORE_PATH):
        with open(STORE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"items": []}


def save_store(store: Dict[str, Any]) -> None:
    with open(STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)


def get_embedding(text: str) -> list[float]:
    resp = client.embeddings.create(
        model="text-embedding-3-small", input=text
    )
    return resp.data[0].embedding


def main() -> None:
    store = load_store()
    existing_ids = {item["id"] for item in store["items"]}

    for path in glob.glob(os.path.join("news", "*.json")):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if data["id"] in existing_ids:
            continue

        text = f"{data['title']}\n\n{data['content']}"
        embedding = get_embedding(text)
        store["items"].append({"id": data["id"], "embedding": embedding})

    save_store(store)


if __name__ == "__main__":
    main()

