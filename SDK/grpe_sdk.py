import subprocess
import os
import platform as pf
import re
import sys
import time
import itertools
import threading
from google import genai
import color as bn

#corefile
####################################################################################################
api = ""
history = []

def set_api(ap):
    global api
    api = ap


def ask_gemini(prompt: str, model_name: str = "gemini-3.5-flash") -> str:
    global api
    api_key = api
    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"


def grpe(code):
    global history
    syst = pf.system()
    prompt = f"OS:{syst} | Command description:{code} | History:{history} | Output ONLY the raw executable command string. Do not include markdown, backticks, explanation, or newlines.If a prompt like \"analyze this\" is received, output the analysis result using `ehco`. If the prompt is prefixed with `(talkmod)`, output the corresponding verbal response using `ehco`."

  
    cd = ask_gemini(prompt)

 
    cd_cleaned = re.sub(r"```[a-zA-Z]*", "", cd)
    cd_cleaned = cd_cleaned.replace("`", "").strip().split("\n")[0]

    if cd_cleaned and "Error" not in cd_cleaned:
        
        result = subprocess.run(cd_cleaned, shell=True, capture_output=True, text=True)
        
        
        output = result.stdout
        
        history.append(f"Prompt:{code}, Executed : {cd}")

        return output 
    else:
        print(f"Failed to parse or execute command: {cd}")
        return None  
