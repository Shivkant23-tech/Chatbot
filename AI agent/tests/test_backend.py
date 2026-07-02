import unittest

from chat_backend import handle_chat_request


class ChatBackendTests(unittest.TestCase):
    def test_chat_request_returns_reply(self):
        response = handle_chat_request({"message": "hello"})
        self.assertIn("reply", response)
        self.assertIn("Hello", response["reply"])

    def test_chat_request_handles_empty_message(self):
        response = handle_chat_request({"message": ""})
        self.assertIn("reply", response)
        self.assertIn("How can I help", response["reply"])

    def test_chat_request_returns_history(self):
        response = handle_chat_request({"message": "hello", "session_id": "history-test"})
        self.assertIn("history", response)
        self.assertEqual(response["history"][-2]["role"], "user")
        self.assertEqual(response["history"][-1]["role"], "assistant")


if __name__ == "__main__":
    unittest.main()
