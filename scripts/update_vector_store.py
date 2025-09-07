"""Upload news items to an OpenAI vector store."""
from __future__ import annotations

import glob
import json
import os
from tempfile import NamedTemporaryFile

from openai import OpenAI


client = OpenAI()
ID_PATH = ".vector_store_id"


def get_vector_store_id() -> str:
    env_id = os.environ.get("VECTOR_STORE_ID")
    if env_id:
        return env_id
    if os.path.exists(ID_PATH):
        with open(ID_PATH, "r", encoding="utf-8") as f:
            return f.read().strip()
    vs = client.vector_stores.create(name="news-items")
    with open(ID_PATH, "w", encoding="utf-8") as f:
        f.write(vs.id)
    return vs.id


def existing_ids(vs_id: str) -> set[str]:
    files = client.vector_stores.files.list(vs_id)
    ids: set[str] = set()
    for f in files.data:
        info = client.files.retrieve(f.id)
        ids.add(os.path.splitext(info.filename)[0])
    return ids


def main() -> None:
    vs_id = get_vector_store_id()
    existing = existing_ids(vs_id)
    for path in glob.glob(os.path.join("news", "*.json")):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if data["id"] in existing:
            continue
        text = f"{data['title']}\n\n{data['content']}"
        with NamedTemporaryFile("w", delete=False, encoding="utf-8") as tmp:
            tmp.write(text)
            tmp_path = tmp.name
        with open(tmp_path, "rb") as f:
            client.vector_stores.files.upload_and_poll(
                vector_store_id=vs_id, file=f
            )
        os.remove(tmp_path)


if __name__ == "__main__":
    main()
