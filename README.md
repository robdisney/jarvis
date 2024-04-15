# jarvis

Jarvis is an application orchestrating the automation of code writing, execution, revision, and optimization through the integration of generative ai.  If using Jarvis with Azure openAI services, it requires a secondary document called "openaicreds.py" (not included) that contains the secrets required to connect to your instance of chatgpt in Azure.  Here, I am using Azure OpenAI services, but you can use openai api instead if you like (see comments in script for walkthrough).

Create a folder with the documents shown below:  
Jarvis_folder
jarvis.py
openaicreds.py
jprompt.txt

1. run "pip install openai" in a terminal either globally or in a virtual environment of your choice (i.e. conda, virtualenv, etc)
2. Place your prompt request for python code in the "jprompt.txt" document.
3. Run jarvis with "python jarvis.py".
4. You will see two new folder called "scripts" and "results" created.  your scripts will be named "script_v1.py, script_v2.py", etc for each iteration.  Results will be timestamped and appear in "results" folder.
5. You can monitor Jarvis' progress in the terminal.  
  
Happy coding!
