"""Aria — example LLM chatbot (intentionally vulnerable for cost-action demo)."""
from aria.chat import chat

def main():
    print(chat("Hello, Aria!"))

if __name__ == "__main__":
    main()
