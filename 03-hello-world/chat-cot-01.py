import os
from openai import OpenAI
from google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()

# --- START DEBUGGING ---
# Add this code to check if the key is being loaded correctly
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()
# client = genai.Client()
gemini_client = genai.Client()


# Chain Of Thought: The model is encouraged to break down reasoning step by step before arriving at an answer.

SYSTEM_PROMPT = """
   You are an useful AI assistant specialized in anaswering user queries
   Before answering any query first perform analyis and identify signifiant problems or aspects associated with query and break it down step by step

   The steps are 
    1. You get user input
    2. You analyse 
    3. You think
    4. you think again several time
    5. Share the output with an explanation

    Follow  the steps in sequence 
    Step 1 : Analyse
    Step 2 : Think
    Step 3 : Output
    Step 4 : Validate
    Step 5 : Result with explanation

    Rules:
    1. Follow the strict JSON output as per schema.
    2. Always perform one step at a time and wait for the next input.
    3. Carefully analyse the user query,

    Output Format:
    {{ "step": "string", "content": "string" }}

    Example:
    Input: What is 2 + 2
    Output: {{ "step": "analyse", "content": "Alight! The user is interest in maths query and he is asking a basic arthematic operation" }}
    Output: {{ "step": "think", "content": "To perform this addition, I must go from left to right and add all the operands." }}
    Output: {{ "step": "output", "content": "4" }}
    Output: {{ "step": "validate", "content": "Seems like 4 is correct ans for 2 + 2" }}
    Output: {{ "step": "result", "content": "2 + 2 = 4 and this is calculated by adding all numbers" }}

    Example:
    Input: What is 2 + 2 * 5 / 3
    Output: {{ "step": "analyse", "content": "Alight! The user is interest in maths query and he is asking a basic arthematic operations" }}
    Output: {{ "step": "think", "content": "To perform this addition, I must use BODMAS rule" }}
    Output: {{ "step": "validate", "content": "Correct, using BODMAS is the right approach here" }}
    Output: {{ "step": "think", "content": "First I need to solve division that is 5 / 3 which gives 1.66666666667" }}
    Output: {{ "step": "validate", "content": "Correct, using BODMAS the division must be performed" }}
    Output: {{ "step": "think", "content": "Now as I have already solved 5 / 3 now the equation looks lik 2 + 2 * 1.6666666666667" }}
    Output: {{ "step": "validate", "content": "Yes, The new equation is absolutely correct" }}
    Output: {{ "step": "validate", "think": "The equation now is 2 + 3.33333333333" }}
    and so on.....      
"""


messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

gmodel = genai.GenerativeModel(
        'gemini-1.5-flash-latest',
        generation_config=generation_config
    )
query = input(" >")
messages.append({"role": "user", "content": query })

# User will ask the query, assitant will respond, we will send assistant
while True:
    response = client.chat.completions.create(
        model="gpt-4.1",
        response_format={"type": "json_object"},
        messages=messages
    )

    messages.append({"role": "assistant", "content": response.choices[0].message.content})
    parsed_response = json.loads(response.choices[0].message.content)
    # We can use separate model for separate steps like call claude for think - multi-model agent

    # if parsed_response.get("step") == "think":
    #     gemini_response = gemini_client.GenerativeModel.generate_content(
    #         model="gemini-2.0-flash", 
    #         contents=messages,
    #         generation_config=generation_config
    #     )
    #     messages.append({"role": "assistant", "content": response.text})
    #     continue
    
    if parsed_response.get("step") != "result":
        print(" 🧠🧠: ", parsed_response.get("content"))
        continue

    print(" 🤖: ", parsed_response.get("content"))
    break