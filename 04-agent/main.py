
import os
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv
import json
import requests
load_dotenv()

client = OpenAI()

# Add context in prompt to return the required dynamic data, otherwise LLM can't have the context
# If we don't add  context it will return static answer
# SYSTEM_PROMPT = f"""
#     You are a helpful AI assistant
#     Today's date is {datetime.now()}
#     Cape Town's weather is  32 degrees
# """
#

# Prompt with weather context using tool
SYSTEM_PROMPT = f"""
    You are and helpful AI assitant who is an expert in resolving query
    You work on start, plan, action, observe mode

    For given user query and available tools, plan step by step execution and based on the planning,
    select the relevant tool from available tools. Based on the tool selection you perform an action to call the tool 

    Wait for the observation and based on the observation from the tool call the resolve the user query

    Rules:
    - Follow the output in JSON format
    - Always perform one step at a time and for next input 
    - Carefully analyse user query

    Output JSON format:
    {{
        "step":"string",
        "content": "string",
        "function": "The name of the function if step in progress",
        "input": "The input parameter for the function",
    }}
    Available tools
    - "get_weather": gets city name as an input and returns the current weather for the city

    Example:
    User Query: What is the weather of Cape Town?
    Output: {{"step": "plan", "content":"The user is intereseted in weather data of Cape Town" }}
    Output: {{"step": "plan", "content":"From available tools should I call get_weather" }}
    Output: {{"step": "action", "function":"get_weather","input":"Cape Town" }}
    Output: {{"step": "observe", "output":"22 Degree celcius" }}
    Output: {{"step": "output", "content":"The temperature of Cape Town seems to be 22 degrees celsius" }}

"""


def get_weather(city: str): 
    # API call to get weather
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    
    return "Weather tool isn't available, try after sometime"


available_tools = {
    "get_weather": get_weather
}

messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]


while True:
    user_query = input("> ")
    messages.append({"role": "user", "content": user_query})

    while True:
        response = client.chat.completions.create(
            model="gpt-4.1",
            response_format={"type": "json_object"},
            messages=messages
        )

        messages.append({"role": "assistant", "content": response.choices[0].message.content})
        parsed_output = json.loads(response.choices[0].message.content)

        if parsed_output.get("step") == "plan":
            print(f"🧠: {parsed_output.get("content")}")

        if parsed_output.get("step") == "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")

            print(f"🛠️: Calling Tool: {tool_name} with input {tool_input}")

            if available_tools.get(tool_name) != False:
                output = available_tools[tool_name](tool_input)
                messages.append({ "role": "user", "content": json.dumps({"step": "observe", "output": output}) })
                continue

        if parsed_output.get("step") == "output": 
            print(f"🤖: {parsed_output.get("content")}")
            break

# response = client.chat.completions.create(
#     model="gpt-4.1",
#     messages=[
#         {"role": "system", "content": SYSTEM_PROMPT},
#         {"role": "user", "content": "What is the weather of Cape Town?"},
#         {"role": "assistant", "content": json.dumps({"step": "plan", "content": "The user is interested in weather data of Cape Town"})},
#         {"role": "assistant", "content": json.dumps({"step": "plan", "content": "From available tools, I should call get_weather to retrieve the current weather for Cape Town."})},
#         {"role": "assistant", "content": json.dumps({"step": "action", "function": "get_weather", "input": "Cape Town"})},
#         {"role": "user", "content": json.dumps({"step": "observe", "output": "-10"})}
#     ]
# )

# print(response.choices[0].message.content)