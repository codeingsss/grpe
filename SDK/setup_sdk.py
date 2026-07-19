import os
import sys
import subprocess

try:
    import pyfiglet
    HAS_PYFIGLET = True
except ImportError:
    HAS_PYFIGLET = False

# ── 색상 (기존 banner 모듈 대체) ──────────────────────────────────────
GREEN = "\033[32m"
BRIGHT_RED = "\033[91m"
RESET = "\033[0m"

# ── 설정값 ────────────────────────────────────────────────────────────
TARGET_SCRIPT = "grpe_sdk.py"   # 현재 경로에 있는, 전역에서 쓰고 싶은 파일
COMMAND_NAME = "grpe_sdk"       # 터미널에서 입력할 명령어 이름 (원하면 변경)


def print_banner():
    title = "GRPE SDK SETUP"
    if HAS_PYFIGLET:
        print(GREEN + pyfiglet.figlet_format(title, font="standard") + RESET)
    else:
        # pyfiglet 미설치 시 대체 출력
        print(f"{GREEN}=== {title} ==={RESET}")
        print(f"{BRIGHT_RED}(pyfiglet이 설치되어 있지 않습니다: pip install pyfiglet){RESET}")

    dot = "·"
    print(f"{GREEN}GRPE SDK {dot} Setup{RESET}")


menu = f"""
{BRIGHT_RED}1. Start Setup
2. Exit GRPE SDK Setup{RESET}
"""


# ── 핵심: 어디서든 실행 가능하게 등록하는 함수 ──────────────────────
def register_script_runner(script_path: str, command_name: str = COMMAND_NAME) -> bool:
    """
    script_path 를 어느 디렉토리에서든 `command_name` 으로 실행할 수 있도록 등록한다.
    - pip install 없이, launcher(래퍼 스크립트)를 PATH 상의 폴더에 생성하는 방식.
    - 한 번 등록하면 터미널을 새로 열 때마다 계속 유지된다.
    """
    home_dir = os.path.expanduser("~")

    if not os.path.isfile(script_path):
        print(f"Error: 대상 파일을 찾을 수 없습니다: {script_path}")
        return False

    # ── Windows ──────────────────────────────────────────────
    if os.name == "nt":
        bin_dir = os.path.join(home_dir, ".grpe", "bin")
        os.makedirs(bin_dir, exist_ok=True)
        launcher_path = os.path.join(bin_dir, f"{command_name}.bat")

        launcher_content = (
            "@echo off\r\n"
            f'python "{script_path}" %*\r\n'
        )
        try:
            with open(launcher_path, "w", encoding="utf-8") as f:
                f.write(launcher_content)
        except Exception as e:
            print(f"Error: launcher 생성 실패: {e}")
            return False

        # 유저 PATH에 bin_dir 영구 등록 (setx)
        try:
            result = subprocess.run(
                ["reg", "query", "HKCU\\Environment", "/v", "Path"],
                capture_output=True, text=True
            )
            existing_path = ""
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if "Path" in line and "REG_" in line:
                        parts = line.split("REG_EXPAND_SZ") if "REG_EXPAND_SZ" in line else line.split("REG_SZ")
                        if len(parts) > 1:
                            existing_path = parts[-1].strip()

            if bin_dir.lower() not in existing_path.lower():
                new_path = f"{existing_path};{bin_dir}" if existing_path else bin_dir
                subprocess.run(["setx", "Path", new_path], check=True)
                print(f"'{bin_dir}' 를 사용자 PATH에 추가했습니다.")
                print("적용을 위해 터미널(cmd/PowerShell)을 새로 열어주세요.")
            else:
                print(f"'{bin_dir}' 는 이미 PATH에 등록되어 있습니다.")
        except Exception as e:
            print(f"Warning: PATH 자동 등록 실패: {e}")
            print(f"다음 폴더를 수동으로 PATH에 추가해주세요: {bin_dir}")

        return True

    # ── macOS / Linux ────────────────────────────────────────
    else:
        bin_dir = os.path.join(home_dir, ".local", "bin")
        os.makedirs(bin_dir, exist_ok=True)
        launcher_path = os.path.join(bin_dir, command_name)

        launcher_content = (
            "#!/usr/bin/env bash\n"
            f'exec python3 "{script_path}" "$@"\n'
        )
        try:
            with open(launcher_path, "w", encoding="utf-8") as f:
                f.write(launcher_content)
            os.chmod(launcher_path, 0o755)
        except Exception as e:
            print(f"Error: launcher 생성 실패: {e}")
            return False

        path_env = os.environ.get("PATH", "")
        if bin_dir not in path_env.split(":"):
            shell = os.environ.get("SHELL", "")
            rc_file = os.path.join(home_dir, ".zshrc") if "zsh" in shell else os.path.join(home_dir, ".bashrc")
            export_line = f'export PATH="{bin_dir}:$PATH"\n'

            try:
                already_added = False
                if os.path.exists(rc_file):
                    with open(rc_file, "r", encoding="utf-8") as f:
                        already_added = bin_dir in f.read()

                if not already_added:
                    with open(rc_file, "a", encoding="utf-8") as f:
                        f.write(f"\n# Added by GRPE SDK Setup\n{export_line}")
                    print(f"'{bin_dir}' 를 PATH에 추가했습니다 ({rc_file}).")
                    print(f"적용하려면 'source {rc_file}' 실행 또는 터미널을 새로 열어주세요.")
                else:
                    print(f"'{bin_dir}' 는 이미 {rc_file} 에 등록되어 있습니다.")
            except Exception as e:
                print(f"Warning: {rc_file} 수정 실패: {e}")
                print(f'다음 줄을 셸 설정 파일에 수동으로 추가해주세요: {export_line.strip()}')
        else:
            print(f"'{bin_dir}' 는 이미 PATH에 등록되어 있습니다.")

        return True


def main():
    print_banner()

    while True:
        print(menu)
        try:
            user = input(f"{GREEN}Select : {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExit..")
            sys.exit()

        if user == "1":
            # __file__ 기준으로 경로를 잡아야 어느 위치에서 실행해도 동작함
            script_path = os.path.abspath(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), TARGET_SCRIPT)
            )
            success = register_script_runner(script_path, COMMAND_NAME)

            if success:
                print("\nSetup Success.")
                print(f"Execute '{COMMAND_NAME}' on terminal or cmd")

                if os.name != "nt":
                    shell = os.environ.get("SHELL", "")
                    rc = "source ~/.zshrc" if "zsh" in shell else "source ~/.bashrc"
                    print(f"Please run {rc} or restart terminal before first use.")
            else:
                print("Setup Failed during Environment registration.")

        elif user == "2":
            print("Exit..")
            sys.exit()

        else:
            print(f"{BRIGHT_RED}Error{RESET}")


if __name__ == "__main__":
    main()