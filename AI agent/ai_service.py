import json
import os
import urllib.error
import urllib.request

from agent import SimpleAIAgent


def build_ollama_payload(message: str, model: str = "llama3.2") -> dict:
    return {"model": model, "prompt": message, "stream": False}


def get_ai_reply(message: str) -> str:
    preferred_model = os.getenv("LOCAL_MODEL", "llama3.2")
    ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

    try:
        payload = build_ollama_payload(message, model=preferred_model)
        req = urllib.request.Request(
            ollama_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=20) as response:
            data = json.load(response)
        if isinstance(data, dict) and data.get("response"):
            return data["response"].strip()
    except (urllib.error.URLError, urllib.error.HTTPError, KeyError, ValueError, TimeoutError):
        pass

    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": message}],
            )
            return response.choices[0].message.content.strip()
        except Exception:
            pass

    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        try:
            endpoint = (
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            )
            payload = {"contents": [{"parts": [{"text": message}]}]}
            req = urllib.request.Request(
                endpoint,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=20) as response:
                data = json.load(response)
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, ValueError, TimeoutError):
            pass

    fallback_agent = SimpleAIAgent(name="Nova")
    return fallback_agent.respond(message)
