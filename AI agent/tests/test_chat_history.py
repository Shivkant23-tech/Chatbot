from chat_backend import SESSION_HISTORY, handle_chat_request


def test_history_is_stored_per_session():
    session_id = "demo-session"
    SESSION_HISTORY.pop(session_id, None)

    first = handle_chat_request({"message": "hello", "session_id": session_id})
    second = handle_chat_request({"message": "how are you", "session_id": session_id})

    assert first["history"][0]["role"] == "user"
    assert second["history"][-1]["role"] == "assistant"
    assert len(SESSION_HISTORY[session_id]) == 4
