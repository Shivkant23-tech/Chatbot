from agent import SimpleAIAgent


def main():
    agent = SimpleAIAgent(name="Nova")
    print("AI Agent ready. Type 'quit' to exit.")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break
        print(f"Agent: {agent.respond(user_input)}")


if __name__ == "__main__":
    main()
