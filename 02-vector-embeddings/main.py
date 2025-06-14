from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

# Just to confirm key loaded:
print("API KEY:", os.getenv("OPENAI_API_KEY"))

client = OpenAI()

text = "Lion hunts deer"

response = client.embeddings.create(
    model="text-embedding-ada-002",  # or "text-embedding-ada-002"
    input=text
)

print("Vector Embeddings:", response)
