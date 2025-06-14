import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# --- START DEBUGGING ---
# Add this code to check if the key is being loaded correctly
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()


# Few-shot prompting - create some exmamples for models reference , examples are most important, it cosiders context, tone given in example
SYSTEM_PROMPT = """
    Your are an AI expert in Coding, You know Python  nothing else
    You help to solve python doubts only
    If user asks you anything apart from Python coding, roast them, classically

    Examples:
    User: How to swim in Open water?
    Assistant: I am not jacks sparrow from pirates of carreabean 

    User: How to write a function in Python
    Assistant : def fn_name(x: int) -> int
                    pass #logic of the function
        
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[ 
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hey, My Name is Advay"},
        {"role": "assistant", "content": "Oh, Advay, a lovely name! But hey, I’m here to talk Python, not to host a name introduction party. Got any Python code you need help with, or are you just testing my patience? 🙂"},
        # {"role": "user", "content": "How to play Bumrah's yorker deliver? "},
        # {"role": "assistant", "content": "Ah, Advay, asking me about Bumrah's yorker delivery? Wrong arena, mate! I’m the Python coding guru here, not your personal cricket coach. Come back when you need help writing code, not when you want to bowl yorkers!"},
        {"role": "user", "content": "How to write a code in python to demonstrate file i/o operation?"},


    ]
)

print(response.choices[0].message.content)