import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# --- START DEBUGGING ---
# Add this code to check if the key is being loaded correctly
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[ 
        {"role": "user", "content": "My Name is Advay"},
        {"role": "assistant", "content": "Hi Advay! How can I assist you today?"},
        {"role": "user", "content": "What's My Name?"},
        {"role": "assistant", "content": "Your name is Advay. How can I help you further?"},
        {"role": "user", "content": "HoW are you?"},

    ]
)

print(response.choices[0].message.content)