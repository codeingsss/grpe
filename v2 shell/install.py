import os
import sys
import banner as bn
import setup as sp

bn.cstm("GRPE SETUP", "standard", bn.GREEN)
dot = "·"
print(f"{bn.GREEN}GRPE V2 {dot} Setup{bn.RESET}")

# 2번과 3번 메뉴 순서 변경
menu = f"""
{bn.BRIGHT_RED}1. Start Setup
2. Change API
3. Exit GRPE v2 Setup{bn.RESET}
"""

def get_api_file_path():
    home_dir = os.path.expanduser("~")
    target_dir = os.path.join(home_dir, ".grpe")
    os.makedirs(target_dir, exist_ok=True)
    return os.path.join(target_dir, "api.grpe")

def mask_key(key: str) -> str:
    if len(key) <= 8:
        return "*" * len(key)
    return f"{key[:4]}{'*' * (len(key) - 8)}{key[-4:]}"

def save_api_key(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                current_api = f.read().strip()
            if current_api:
                print(f"Current API Key: {mask_key(current_api)}")
        except Exception:
            pass

    try:
        api = input(f"{bn.GREEN}New Gemini API : {bn.RESET}").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nAPI Key entry cancelled.")
        return False

    if not api:
        print("API Key entry cancelled.")
        return False

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(api)
        if os.name != "nt":
            os.chmod(path, 0o600)  # 소유자만 읽기/쓰기 가능하도록 권한 제한
        print(f"API Key saved at: {path}")
        return True
    except Exception as e:
        print(f"Error Failed to save API Key: {e}")
        return False

def main():
    while True:
        print(menu)
        try:
            user = input(f"{bn.GREEN}Select : {bn.RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExit..")
            sys.exit()

        if user == "1":
            # __file__ 기준으로 경로를 잡아야 어느 위치에서 실행해도 동작함
            script_path = os.path.abspath(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "grpe.py")
            )
            success = sp.register_script_runner(script_path)

            if success:
                api_path = get_api_file_path()
                if save_api_key(api_path):
                    print("\nSetup Success.")
                    print("Execute grpe on terminal or cmd")

                    if os.name != 'nt':
                        shell = os.environ.get("SHELL", "")
                        rc = "source ~/.zshrc" if "zsh" in shell else "source ~/.bashrc"
                        print(f"Please run {rc} or restart terminal before first use.")
                else:
                    print("Setup Failed during API saving.")
            else:
                print("Setup Failed during Environment registration.")

        elif user == "2":
            # 2번 메뉴: API 수정 기능
            api_path = get_api_file_path()
            print("\nChanging API Key...")
            if save_api_key(api_path):
                print("API Key updated successfully.")
            else:  
                print("API Key update failed.")

        elif user == "3":
            # 3번 메뉴: 종료 기능
            print("Exit..")
            sys.exit()

        else:
            print(f"{bn.BRIGHT_RED}Error{bn.RESET}")

if __name__ == "__main__":
    main()