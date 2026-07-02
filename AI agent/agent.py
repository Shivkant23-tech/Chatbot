class SimpleAIAgent:
    def __init__(self, name="Agent"):
        self.name = name

    def respond(self, user_input: str) -> str:
        text = (user_input or "").strip()
        if not text:
            return f"How can I help you today? I’m {self.name}."

        lower_text = text.lower()
        if "hello" in lower_text or "hi" in lower_text:
            return f"Hello! I’m {self.name}, and I can answer questions, explain ideas, and help with tasks."

        if any(keyword in lower_text for keyword in ["help", "plan", "project", "study", "learn", "code", "python", "java", "write", "explain"]):
            return (
                f"I can help with that. I’m {self.name}, and I can explain concepts, draft content, "
                f"assist with coding, or help you plan and break a task into steps."
            )

        if any(keyword in lower_text for keyword in ["weather", "time", "date", "capital", "who", "what", "why", "how"]):
            return (
                f"That’s a great question. I’m {self.name}, and I can provide a helpful explanation or summary "
                f"based on what you ask."
            )

        return (
            f"Thanks for asking. I’m {self.name}, and I can help answer questions, explain ideas, "
            f"and support your work in a clear and practical way."
        )
