# chat_with_json_latest_sdk.py
import os
import json
# --- Step 1: Use the latest SDK import ---
# This is the import for the newer 'google-genai' package.
from google import genai
from dotenv import load_dotenv, find_dotenv

# --- Step 2: Load and Configure the API Key ---
# This part remains the same. It loads your GOOGLE_API_KEY from the .env file.
print("--- Debugging Environment ---")
print(f"Current Working Directory: {os.getcwd()}")
print(f"Looking for .env file at: {find_dotenv() or 'Not Found'}")

# Load environment variables from .env file.
# load_dotenv() returns True if it found and loaded a file, False otherwise.
was_env_loaded = load_dotenv()
print(f".env file loaded successfully: {was_env_loaded}")
print("---------------------------")


print("\nAttempting to load API Key from .env file...")

try:
    # Configure the 'genai' library with your API key.
    # This is now the standard setup step.
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    print("🟢 API Key configured successfully.")
except (KeyError, AttributeError):
    print("🔴 Error: GOOGLE_API_KEY not found or invalid. Please check your .env file.")
    exit()

# --- Step 3: Define the Generation Configuration for JSON ---
# This dictionary tells the model that we expect the response to be in JSON format.
generation_config = {
    "response_mime_type": "application/json",
}

# --- Step 4: Initialize the Model ---
# We now initialize the model directly after configuration.
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest"
)
print("🤖 Model initialized.")


# --- Step 5: Define a Clear Prompt ---
# It's still a best practice to describe the desired JSON structure in the prompt.
prompt = """
Generate a JSON object for a software development team profile. The object should have three keys: 
'team_name', 'project', and 'members'. 
'members' key should be an array of objects, where each object has a 'name' and a 'role'.
Please create a profile for a team named 'InnovateAI' working on a 'GenAI Chatbot'.
Include two members: 'Advay' as 'Staff Engineer' and 'Priya' as 'Data Scientist'.
"""

# --- Step 6: Generate Content and Parse the Response ---
# The 'generation_config' is passed here, in the 'generate_content' method.
print("\nSending prompt to Gemini...")
try:
    response = model.generate_content(
        contents=prompt,
        generation_config=generation_config # The config is passed here
    )

    print("\n--- Raw JSON Response from API ---")
    # The response object structure is the same, so .text still works perfectly.
    print(response.text)

    # --- Step 7: Load the JSON string into a Python dictionary ---
    data = json.loads(response.text)

    print("\n--- Parsed Python Dictionary ---")
    print(data)

    print("\n--- Accessing Data from the Dictionary ---")
    print(f"Team Name: {data['team_name']}")
    print(f"Project: {data['project']}")
    for member in data['members']:
        print(f"  - Member: {member['name']}, Role: {member['role']}")

except Exception as e:
    print(f"\n🔴 An error occurred while generating content: {e}")
