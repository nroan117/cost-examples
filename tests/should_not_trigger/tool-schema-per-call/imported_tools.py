import openai
from my_tools import TOOLS  # imported from another module

client = openai.OpenAI()

def handle(msg):
    # Good: tools imported from module level
    client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": msg}], tools=TOOLS, max_tokens=200)
