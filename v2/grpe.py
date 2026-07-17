#!/usr/bin/env python3
import grpe_cli as ge
import banner as bn
import os
import sys

bn.bnr()
dot = "·"
print(f"{bn.GREEN}GRPE V2 {dot} Shell{bn.RESET}")
print()


if os.name == "nt":
    home_dir = os.environ.get("USERPROFILE") or os.path.expanduser("~")
else:
    home_dir = os.environ.get("HOME") or os.path.expanduser("~")

api_path = os.path.join(home_dir, ".grpe", "api.grpe")

# 파일이 없는 경우 예외 처리
if not os.path.exists(api_path):
    print("Error API key not found. Please run setup script first.")
    sys.exit(1)

# API 키 읽기
try:
    with open(api_path, "r", encoding="utf-8") as f:
        GEMINI_API_KEY = f.read().strip()
    
    if not GEMINI_API_KEY:
        print("Error API key file is empty. Please register a valid key.")
        sys.exit(1)
        
except Exception as e:
    print(f"Error Failed to read API key file: {e}")
    sys.exit(1)

# API 설정 적용
ge.set_api(GEMINI_API_KEY)

while True:
    user = input(f"{bn.BRIGHT_BLACK}{sys.argv[0]} : {bn.RESET}")
    ge.exect(user)