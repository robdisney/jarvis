""" Use this version if you are using ChatGPT from Azure OpenAI Services """

# jarvis.py

# Import libraries
import subprocess
import os
from datetime import datetime
from pathlib import Path
from openai import AzureOpenAI
import re
from openaicreds import openaiapi_version, openaiapi_base, openaiapi_key, model

client = AzureOpenAI(api_version=openaiapi_version,
                     azure_endpoint=openaiapi_base,
                     api_key=openaiapi_key)

# Define function to extract python code from responses
def extract_python(response_content):
    # Define the regular expression pattern for extracting Python code blocks
    pattern = r"```python(.*?)```"
    # Use re.DOTALL to make the dot match newlines as well
    match = re.search(pattern, response_content, re.DOTALL)
    if match:
        # Extract the code, remove leading/trailing whitespace, and return
        return match.group(1).strip()
    elif 'satisfied' in response_content.lower():
        return 'satisfied'
    else:
        return None
    
# Define the function to extract any "pip install" statement from chatgpt response and then install via subprocess before attempting running python script.
def handle_pip_install(response_content):
    # Define the regular expression pattern for extracting pip install commands
    pattern = r"pip install (.*?)\n"
    match = re.search(pattern, response_content, re.DOTALL)
    if match:
        # Extract the command, remove leading/trailing whitespace, and return
        command = match.group(1).strip()
        command = "pip install " + command
        print(f"Executing '''bash\n{command}\n'''")
        # Use subprocess to execute the command
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        # Fetch the output and errors, if any
        output, error = process.communicate()
        # Print the command's output
        print('Output:', output.decode())
        # Print the command's error
        if error:
            print('Error:', error.decode())

# Define the function to generate a response from the AI
def generate_response(prompt):
    response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}],
                                              model=model,
                                              max_tokens=4000,
                                              temperature=0.75) 
    return response.choices[0].message.content

# Function to read the latest prompt and append the additional phrase
def read_latest_prompt():
    prompt_content = Path('prompts/prompt.txt').read_text('utf-8')
    additional_phrase = "\nReturn your response as a complete python script. The code you return must be a complete solution. Ensure that if you use print statements, they are not commented out, regardless of the original prompt request."
    return f"{prompt_content}{additional_phrase}"

# Function to write the Python script to a file
def write_script_to_file(script, version):
    filename = f'scripts/script_v{version}.py'
    with open(filename, 'w') as file:
        file.write(script)
    return filename

# Function to execute the Python script and capture its output
def execute_script(filename):
    try:
        result = subprocess.run(['python', filename], capture_output=True, text=True, check=True)
        return result.stdout, None
    except subprocess.CalledProcessError as e:
        # Return both stdout and stderr if an error occurs
        return e.stdout, e.stderr

# Function to write the result to a file with a timestamp
def write_result_to_file(output):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'results/results_{timestamp}.txt'
    with open(filename, 'w') as file:
        file.write(output)
    return filename, timestamp

# Main loop for generating, executing, and validating the script
def main_loop():
    version = 1
    original_prompt = read_latest_prompt()

    while True:
        # Generate the response from AI
        prompt = original_prompt if version == 1 else combined_prompt
        print(f'sending prompt to chatgpt iteration {version}')
        response = generate_response(prompt)
        print(f"ChatGPT's response for iteration {version} is: \n", response)

        # Handle pip install commands in the response
        handle_pip_install(response)

        # Check if AI is satisfied or if there's a Python script to extract
        extracted_code = extract_python(response)
        print('extracted code:\n', extracted_code)
        if extracted_code == 'satisfied':
            print("AI is satisfied with the script.")
            break
        elif extracted_code is None:
            print("No Python script found in AI response.")
            continue  # Continue to the next iteration instead of breaking

        # Write the new script version
        script_filename = write_script_to_file(extracted_code, version)
        print(f"Script version {version} written to {script_filename}.")

        # Execute the new script version
        output, error = execute_script(script_filename)
        execution_outcome = output, error

        # Write the output or error to a timestamped results file
        if error:
            result_filename, _ = write_result_to_file(f"Error executing script:\n{error}")
            print(f"Error executing script: Check {result_filename} for details.")
        else:
            result_filename, _ = write_result_to_file(output)
            print(f"Script version {version} executed. Check {result_filename} for the output.")

        # Prepare the prompt for the next iteration
        combined_prompt = f"You were asked: {original_prompt}\n\n# and produced this script:\n{extracted_code}\n\n# which produced these Results:\n{execution_outcome}\n\nBased on what you were asked to do, the script you wrote, and its results, are you satisfied? If yes, return only the word 'satisfied'. If no, revise the script to achieve the desired results. in your response, return the entire revised script.  If your code requires any libaries that need to be installed for the code to work, include a single 'pip install' command to install them."
        print(f"Sending the following prompt to AI:\n{combined_prompt}")

        version += 1

# Run the main loop
if __name__ == "__main__":
    main_loop()
