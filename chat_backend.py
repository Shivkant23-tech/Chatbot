from ai_service import get_ai_reply
from document_utils import build_context_with_document

SESSION_HISTORY = {}
MEMORY_SUMMARIES = {}


def _build_context(history: list[dict], message: str) -> str:
    recent = history[-8:] if history else []
    if not recent:
        return message

    context_lines = []
    for item in recent:
        role = item.get("role", "user")
        content = item.get("content", "")
        if content:
            context_lines.append(f"{role}: {content}")

    context_lines.append(f"user: {message}")
    return "\n".join(context_lines)


def _update_memory_summary(session_id: str, history: list[dict]) -> str:
    summary = MEMORY_SUMMARIES.get(session_id, "")
    if not history:
        return summary

    recent_items = [item for item in history[-6:] if item.get("content")]
    if not recent_items:
        return summary

    turns = []
    for item in recent_items:
        turns.append(f"{item.get('role', 'user')}: {item.get('content', '')}")

    combined = " | ".join(turns)
    if summary:
        return f"{summary} | {combined}"
    return combined


def handle_chat_request(payload: dict) -> dict:
    payload = payload or {}
    message = payload.get("message", "")
    session_id = payload.get("session_id") or "default"

    history = SESSION_HISTORY.setdefault(session_id, [])
    if message.strip():
        history.append({"role": "user", "content": message.strip()})

    document_text = payload.get("document_text", "")
    message_for_model = build_context_with_document(message, document_text)
    context_message = _build_context(history, message_for_model)
    reply = get_ai_reply(context_message)
    history.append({"role": "assistant", "content": reply})

    MEMORY_SUMMARIES[session_id] = _update_memory_summary(session_id, history)

    return {"reply": reply, "history": history, "memory_summary": MEMORY_SUMMARIES[session_id]}
