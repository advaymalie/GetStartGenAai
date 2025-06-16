import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

# --- START DEBUGGING ---
# Add this code to check if the key is being loaded correctly
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()


# Chain of thoughts - The model is encouraged to break down reasoning step by step before arriving at answer
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

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    response_format={"type":"json_object"},
    messages=[ 
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "What is 5/2 * 3 to the power of 4"},
        {"role": "assistant", "content": json.dumps({ "step": "analyse", "content": "The user is interested in solving a mathematical expression containing division, multiplication and exponentiation operations: 5/2 * 3^4." })},
        {"role": "assistant", "content": json.dumps({"step": "think", "content": "To solve 5/2 * 3^4, I must follow the order of operations (BODMAS/BIDMAS): first calculate the exponent (3^4), then perform the division and multiplication from left to right."})},
        {"role": "assistant", "content": json.dumps({"step": "output", "content": "First calculate 3^4, which is 3 * 3 * 3 * 3 = 81. Then calculate 5/2 = 2.5. Finally multiply 2.5 * 81 = 202.5."})},
        {"role": "assistant", "content": json.dumps({"step": "validate", "content": "The steps are consistent with the order of operations rule, and the calculations for 3^4 and 5/2 are correct. The multiplication result 2.5 * 81 equals 202.5, so this answer is accurate."})},
        {"role": "assistant", "content": json.dumps({"step": "result", "content": "The value of the expression 5/2 * 3^4 is 202.5. This was calculated by first evaluating the exponent to get 81, then calculating 5 divided by 2 to get 2.5, and finally multiplying these two results."})},
    ]
    
)

print("\n\n🤖=>", response.choices[0].message.content, "\n")