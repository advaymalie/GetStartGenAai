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
        {"role": "user", "content": "Hello there"}
    ]
)

print(response.choices[0].message.content)