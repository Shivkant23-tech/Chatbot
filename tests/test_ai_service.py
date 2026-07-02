from ai_service import build_ollama_payload


def test_build_ollama_payload_uses_selected_model():
    payload = build_ollama_payload("hello", model="llama3.2")
    assert payload["model"] == "llama3.2"
    assert payload["prompt"] == "hello"
    assert payload["stream"] is False
