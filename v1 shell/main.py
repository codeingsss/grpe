import banner as bn
import sys
import grpe_cli as exe
import os
bn.bnr()
print(f"{bn.GREEN}GRPE V1 · SettingPage{bn.RESET}")
menu = """
1. Set API Key
2. Start
"""
print(menu)
while True:
    chse = input(f"{bn.GREEN}Select : {bn.RESET}")
    if chse == "1":
        api = input(f"{bn.GREEN}Input API : {bn.RESET}")
        f = open("api.grpe", "w", encoding="utf-8")
        f.write(api)
        f.close()
        break
    elif chse == "2":
        break


os.system('cls' if os.name == 'nt' else 'clear')


bn.bnr()
print(f"{bn.GREEN}GRPE V1 · Shell{bn.RESET}")

while True:
    user = input(f"{bn.GREEN}{sys.argv[0]}{bn.RESET} : ")
    exe.exect(user)
    