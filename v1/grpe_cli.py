import subprocess
import os
import platform as pf
import re
import sys
import time
import itertools
import threading
from google import genai
import banner as bn

f = open("api.grpe", "r", encoding="utf-8")
api = f.read()
history = []


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


def spinner_animation(stop_event):
    for ch in itertools.cycle(['\\', '|', '/', '-']):
        if stop_event.is_set():
            break
        sys.stdout.write(f"\r{bn.BLUE}{ch} Generating...{bn.RESET}")
        sys.stdout.flush()
        time.sleep(0.1)
    # 스피너 라인 지우기
    sys.stdout.write("\r" + " " * 30 + "\r")
    sys.stdout.flush()


def exect(code):
    global history
    syst = pf.system()
    prompt = f"OS:{syst} | Command description:{code} | History:{history} | Output ONLY the raw executable command string. Do not include markdown, backticks, explanation, or newlines."
    
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner_animation, args=(stop_event,))
    spinner_thread.start()
    
    try:
        cd = ask_gemini(prompt)
    finally:
        stop_event.set()
        spinner_thread.join()
        
    # 응답에서 마크다운 백틱이나 줄바꿈을 완벽히 지워주는 청소 로직
    cd_cleaned = re.sub(r"```[a-zA-Z]*", "", cd)
    cd_cleaned = cd_cleaned.replace("`", "").strip().split("\n")[0]
    
    if cd_cleaned and "Error" not in cd_cleaned:
        os.system(cd_cleaned)
        history.append(f"Prompt:{code}, Executed : {cd}")
        
        # 10글자가 넘으면 자르고 '...'을 붙이는 로직
        cd_display = cd_cleaned if len(cd_cleaned) <=30 else cd_cleaned[:10] + "..."
        print(f"{bn.RED}Executed :{bn.RESET}{bn.BLUE} {cd_display}{bn.RESET}")
    else:
        print(f"Failed to parse or execute command: {cd}")


def cli(code):
    global history
    syst = pf.system()
    prompt = f"OS:{syst} | Command description:{code} | History:{history} | Output ONLY the raw executable command string. Do not include markdown, backticks, explanation, or newlines."

    # AI API 호출
    cd = ask_gemini(prompt)

    # 응답 청소 로직
    cd_cleaned = re.sub(r"```[a-zA-Z]*", "", cd)
    cd_cleaned = cd_cleaned.replace("`", "").strip().split("\n")[0]

    if cd_cleaned and "Error" not in cd_cleaned:
        # subprocess를 이용해 명령어를 실행하고 출력을 문자열로 캡처
        result = subprocess.run(cd_cleaned, shell=True, capture_output=True, text=True)
        
        # 실행 결과(정상 출력)를 가져옴
        output = result.stdout
        
        history.append(f"Prompt:{code}, Executed : {cd}")
        print(f"{bn.RED}Executed :{bn.RESET}{bn.BLUE} {cd_cleaned}{bn.RESET}")
        
        return output  # 콘솔 출력 리턴
    else:
        print(f"Failed to parse or execute command: {cd}")
        return None  # 실패 시 None 리턴
