from chat_backend import handle_chat_request, SESSION_HISTORY


def test_context_is_used_across_turns():
    session_id = "context-session"
    SESSION_HISTORY.pop(session_id, None)

    first = handle_chat_request({"message": "My name is Alex", "session_id": session_id})
    second = handle_chat_request({"message": "What is my name?", "session_id": session_id})

    assert first["history"][0]["role"] == "user"
    assert second["history"][-1]["role"] == "assistant"
    assert len(SESSION_HISTORY[session_id]) == 4
