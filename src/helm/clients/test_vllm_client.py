import sys
import types

fake_openai = types.ModuleType("openai")


class FakeOpenAIError(Exception):
    pass


class PlaceholderOpenAI:
    def __init__(self, **kwargs):
        pass


fake_openai.OpenAIError = FakeOpenAIError
fake_openai.OpenAI = PlaceholderOpenAI
sys.modules.setdefault("openai", fake_openai)

from helm.clients.vllm_client import VLLMClient
from helm.common.cache import BlackHoleCacheConfig


def test_vllm_client_does_not_leak_tokenizer_kwargs_to_openai(monkeypatch):
    observed = {}

    class FakeOpenAI:
        def __init__(self, **kwargs):
            observed["kwargs"] = dict(kwargs)

    monkeypatch.setattr("helm.clients.openai_client.OpenAI", FakeOpenAI)

    tokenizer = object()
    client = VLLMClient(
        tokenizer=tokenizer,
        tokenizer_name="hf-internal-testing/llama-tokenizer",
        cache_config=BlackHoleCacheConfig(),
        base_url="http://127.0.0.1:8000/openai/v1",
        vllm_model_name="vicuna-7b-v1-3-no-chat-template",
    )

    assert client.tokenizer is tokenizer
    assert client.tokenizer_name == "hf-internal-testing/llama-tokenizer"
    assert observed["kwargs"]["api_key"] == "EMPTY"
    assert observed["kwargs"]["base_url"] == "http://127.0.0.1:8000/openai/v1"
    assert "tokenizer" not in observed["kwargs"]
    assert "tokenizer_name" not in observed["kwargs"]
