from agent import SimpleAIAgent


def test_general_question_response_is_helpful():
    agent = SimpleAIAgent(name="Nova")
    reply = agent.respond("What is Python?")
    assert "help" in reply.lower() or "explain" in reply.lower() or "question" in reply.lower()
