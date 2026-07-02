from chat_backend import MEMORY_SUMMARIES, SESSION_HISTORY, handle_chat_request


def test_memory_summary_is_stored_per_session():
    session_id = "memory-session"
    SESSION_HISTORY.pop(session_id, None)
    MEMORY_SUMMARIES.pop(session_id, None)

    response = handle_chat_request({"message": "My name is Alex", "session_id": session_id})

    assert "memory_summary" in response
    assert session_id in MEMORY_SUMMARIES
    assert "Alex" in MEMORY_SUMMARIES[session_id]
