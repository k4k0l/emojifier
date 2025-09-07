import os
import pytest
from openai import OpenAI


def test_models_list():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set")
    client = OpenAI(api_key=api_key)
    models = client.models.list()
    assert len(models.data) > 0
