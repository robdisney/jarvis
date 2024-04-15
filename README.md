# jarvis

Jarvis is an application orchestrating the automation of code writing, execution, revision, and optimization through the integration of generative ai.  If using Jarvis with Azure openAI services, it requires a secondary document called "openaicreds.py" (not included) that contains the secrets required to connect to your instance of chatgpt in Azure.  Here, I am using Azure OpenAI services, but you can use openai api instead if you like (see comments in script for walkthrough).

The folder Jarvis is in requires three additional folders:  prompts (with prompt.txt), results, and scripts.  Place your prompt in the "prompts.txt" document, run jarvis.py (after openai library is installed) and then run "python jarvis.py".  You will see your scripts written under "scripts" as "script_v1.py, script_v2.py", etc.  Results will be timestamped as well.  
for example:

your_folder
- jarvis.py
- openaicreds.py
  prompts
  - prompt.txt
  scripts
  results

Happy coding!
