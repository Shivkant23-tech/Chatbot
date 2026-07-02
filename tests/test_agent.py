import unittest

from agent import SimpleAIAgent


class SimpleAIAgentTests(unittest.TestCase):
    def setUp(self):
        self.agent = SimpleAIAgent(name="Nova")

    def test_greeting_response(self):
        reply = self.agent.respond("hello")
        self.assertIn("Hello", reply)
        self.assertIn("Nova", reply)

    def test_task_help_response(self):
        reply = self.agent.respond("help me plan a project")
        self.assertIn("plan", reply.lower())

    def test_empty_input_response(self):
        reply = self.agent.respond("")
        self.assertIn("How can I help", reply)


if __name__ == "__main__":
    unittest.main()
