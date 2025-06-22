
import os
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv
import json
import requests
import sys 
from typing import Dict, Any, List
import subprocess
import os
load_dotenv()

client = OpenAI()


# Prompt with weather context using tool
SYSTEM_PROMPT = f"""
    You are an expert coder with good understanding of 
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
    - "create_file": Creates a new file at the specified path with the given content. If the directories in the path don't exist, they will be created
    - "read_file":  Reads and returns the content of the specified file
    - "list_files": Lists all files and directories in the specified directory
    - "run_command": Executes a linux command and returns its output and errors
    - "install_package": Installs a Python package using pip
    - "git_diff": Runs 'git diff' to see the current unstaged changes in the repository,

    Example 1: create_file
        User Query: Create a file named 'app.py' and add a simple print statement to it.

        Output: {{"step": "plan", "content": "The user wants to create a new Python file with some initial content. I will use the create_file tool."}}
        Output: {{"step": "plan", "content": "The file name should be 'app.py' and the content will be 'print(\"Hello, AdvayCode!\")'."}}
        Output: {{"step": "action", "function": "create_file", "input": "file_path": "app.py", "content": "print(\"Hello, AdvayCode!\")"}}
        Output: {{"step": "observe", "output": "Successfully created file: app.py"}}
        Output: {{"step": "output", "content": "I have successfully created the file 'app.py' with a print statement inside."}}

    Example 2: read_file
        Output: {{"step": "plan", "content": "The user wants to read the content of a file. I need to use the read_file tool."}}
        Output: {{"step": "action", "function": "read_file", "input": "app.py"}}
        Output: {{"step": "observe", "output": "print(\"Hello, AdvayCode!\")"}}
        Output: {{"step": "output", "content": "The file 'app.py' contains the following code: print(\"Hello, AdvayCode!\")"}}

    Example 3: list_files
        User Query: What files are in the current directory?

        Output: {{"step": "plan", "content": "The user wants to see the files in the current directory. I should use the list_files tool."}}
        Output: {{"step": "action", "function": "list_files", "input": "."}}
        Output: {{"step": "observe", "output": "main.py\nREADME.md\n.gitignore"}}
        Output: {{"step": "output", "content": "I found the following files in the current directory: main.py, README.md, and .gitignore."}}

    Example 4: run_command
        User Query: What version of python am I using?

        Output: {{"step": "plan", "content": "The user is asking for the system's Python version. I can find this by executing a shell command. The run_command tool is appropriate for this."}}
        Output: {{"step": "action", "function": "run_command", "input": "python --version"}}
        Output: {{"step": "observe", "output": "Python 3.11.2"}}
        Output: {{"step": "output", "content": "You are currently using Python version 3.11.2."}}

    Example 5: install_package
        User Query: I need to work with APIs, please install the requests package.

        Output: {{"step": "plan", "content": "The user needs a package for making API calls. The 'requests' library is standard for this. I will use the install_package tool."}}
        Output: {{"step": "action", "function": "install_package", "input": "requests"}}
        Output: {{"step": "observe", "output": "Successfully installed requests-2.28.1"}}
        Output: {{"step": "output", "content": "The 'requests' package has been successfully installed."}}

    Example 6: git_diff
        User Query: Show me the changes I've made since my last commit.

        Output: {{"step": "plan", "content": "The user wants to see their current unstaged changes. I should use the git_diff tool for this."}}
        Output: {{"step": "action", "function": "git_diff", "input": null}}
        Output: {{"step": "observe", "output": "diff --git a/app.py b/app.py\nindex e69de29..a24915a 100644\n--- a/app.py\n+++ b/app.py\n@@ -0,0 +1 @@\n+print(\"Hello, AdvayCode!\")"}}
        Output: {{"step": "output", "content": "You have one change: the file 'app.py' was modified to add a print statement."}}

    Example 7: Create a new Full-Stack "Hello World" Application with a Python/Flask backend and a React/Vite frontend.

        Output: {{"step": "plan", "content": "The user wants a simple 'Hello World' app. I'll start by creating a unique project directory using a timestamp to avoid conflicts."}}
        Output: {{"step": "action", "function": "run_command", "input": "mkdir hello-world-app-$(date +%s)"}}
        Output: {{"step": "observe", "output": "Successfully created directory: hello-world-app-1749821300"}}

        Output: {{"step": "plan", "content": "Now, inside the new project folder, I will set up the simple Python backend."}}
        Output: {{"step": "action", "function": "run_command", "input": "cd hello-world-app-1749821300 && mkdir server && cd server"}}
        Output: {{"step": "observe", "output": "Successfully changed directory and created server subdirectory."}}

        Output: {{"step": "plan", "content": "I will initialize a Python virtual environment and create a requirements file."}}
        Output: {{"step": "action", "function": "run_command", "input": "python -m venv venv"}}
        Output: {{"step": "observe", "output": "Successfully created virtual environment."}}
        Output: {{"step": "action", "function": "create_file", "input": {{"file_path": "requirements.txt", "content": "Flask\\nFlask-Cors"}}}}
        Output: {{"step": "observe", "output": "Successfully created requirements.txt."}}

        Output: {{"step": "plan", "content": "Now I will create a single 'app.py' file for the backend with one API endpoint that returns a greeting."}}
        Output: {{"step": "action", "function": "create_file", "input": {{"file_path": "app.py", "content": "from flask import Flask, jsonify\\nfrom flask_cors import CORS\\n\\napp = Flask(__name__)\\nCORS(app)  # Enable CORS for React dev server\\n\\n@app.route('/api/hello', methods=['GET'])\\ndef get_greeting():\\n    return jsonify({{\"message\": \"Hello from your Python Backend!\"}})\\n\\nif __name__ == '__main__':\\n    app.run(debug=True)"}}}}
        Output: {{"step": "observe", "output": "Successfully created backend app.py file."}}

        Output: {{"step": "plan", "content": "The backend is set up. I will now set up the React frontend using Vite."}}
        Output: {{"step": "action", "function": "run_command", "input": "cd ../ && npm create vite@latest client -- --template react"}}
        Output: {{"step": "observe", "output": "Successfully created Vite project in 'client' directory."}}

        Output: {{"step": "plan", "content": "I will now edit the main App.jsx file to fetch the greeting from the backend and display it."}}
        Output: {{"step": "action", "function": "create_file", "input": {{"file_path": "client/src/App.jsx", "content": "import React, {{ useState, useEffect }} from 'react';\\n\\nfunction App() {{\\n    const [message, setMessage] = useState('');\\n\\n    useEffect(() => {{\\n        fetch('http://127.0.0.1:5000/api/hello')\\n            .then(res => res.json())\\n            .then(data => setMessage(data.message));\\n    }}, []);\\n\\n    return (\\n        <div>\\n            <h1>Full-Stack Hello World</h1>\\n            <p>Message from backend: <strong>{{message}}</strong></p>\\n        </div>\\n    );\\n}}\\n\\nexport default App;"}}}}
        Output: {{"step": "observe", "output": "Successfully updated App.jsx."}}

        Output: {{"step": "plan", "content": "The project structure is complete. I will now provide the final instructions for the user."}}
        Output: {{"step": "output", "content": "The 'Hello World' application has been successfully created. To run the backend: 1. Navigate to the serverdirectory. 2. Activate the virtual environment:source venv/bin/activate. 3. Install packages: pip install -r requirements.txt. 4. Run the server: python app.py. To run the frontend: 1. Navigate to the clientdirectory in a new terminal. 2. Runnpm installfirst. 3. Run the development server:npm run dev."}}
"""



# def run_command(cmd: str):
#     result = os.system(cmd)
#     return result


def create_file(file_path: str, content: str = "") -> str:
    """
    Creates a new file at the specified path with the given content.
    If the directories in the path don't exist, they will be created.
    """
    try:
        # Create the directory structure if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully created file: {file_path}"
    except Exception as e:
        return f"Error creating file: {e}"


def read_file(file_path: str) -> str:
    """
    Reads and returns the content of the specified file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"Error: File not found at {file_path}"
    except Exception as e:
        return f"Error reading file: {e}"


def list_files(directory: str = '.') -> str:
    """
    Lists all files and directories in the specified directory.
    """
    try:
        if not os.path.isdir(directory):
            return f"Error: '{directory}' is not a valid directory."
        
        files = os.listdir(directory)
        if not files:
            return f"The directory '{directory}' is empty."
        
        return "\n".join(files)
    except Exception as e:
        return f"Error listing files: {e}"



def run_command(command: str) -> str:
    """
    Executes a shell command and returns its output and errors.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=False,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return f"Command executed successfully.\nOutput:\n{result.stdout}"
        else:
            return f"Command failed with return code {result.returncode}.\nError:\n{result.stderr}"
    except Exception as e:
        return f"An error occurred while trying to run the command: {e}"


def install_package(package_name: str) -> str:
    """
    Installs a Python package using pip.
    """
    # Use sys.executable to ensure we're using the pip from the current Python environment
    command = f'"{sys.executable}" -m pip install {package_name}'
    return run_command(command)


def git_diff() -> str:
    """
    Runs 'git diff' to see the current unstaged changes in the repository.
    """
    command = "git diff"
    return run_command(command)


# The final dictionary mapping tool names to their function definitions
available_tools: Dict[str, Any] = {
    # File System
    "create_file": create_file,
    "read_file": read_file,
    "list_files": list_files,
    
    # Command Execution
    "run_command": run_command,
    "install_package": install_package,
    "git_diff": git_diff,
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