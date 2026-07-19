import os
import sys
import json
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


# ── 추가: 어디서든 import 가능하게 등록하는 함수 ──────────────────────
def register_module_path(module_dir: str) -> bool:
    """
    module_dir 를 현재 python 인터프리터의 site-packages 에 .pth 파일로 등록해서
    어느 스크립트에서든 `import grpe_sdk` 가 되도록 한다.
    - .pth 파일은 파이썬이 시작할 때마다 자동으로 읽어 sys.path 에 추가해준다.
    - 셸(bash/zsh) 설정과 무관하게, 이 인터프리터로 실행되는 모든 파이썬 코드에 적용된다.
    - 주의: pyenv/homebrew/venv 등 파이썬이 여러 개라면, 각 인터프리터마다 따로 등록해야 한다.
      (지금 이 스크립트를 실행 중인 python 에만 등록됨)
    """
    try:
        import site
        site_packages_candidates = site.getsitepackages()
    except Exception:
        site_packages_candidates = []

    # getsitepackages()가 비어있는 경우(venv 등) 대비
    if not site_packages_candidates:
        try:
            import sysconfig
            site_packages_candidates = [sysconfig.get_paths()["purelib"]]
        except Exception:
            print("Error: site-packages 경로를 찾을 수 없습니다.")
            return False

    target_dir = None
    for candidate in site_packages_candidates:
        if os.path.isdir(candidate) and os.access(candidate, os.W_OK):
            target_dir = candidate
            break

    if target_dir is None:
        print("Error: 쓰기 가능한 site-packages 경로를 찾지 못했습니다.")
        print(f"현재 python: {sys.executable}")
        return False

    pth_path = os.path.join(target_dir, "grpe_sdk.pth")

    try:
        # 이미 같은 경로로 등록돼 있으면 중복 작성 방지
        if os.path.exists(pth_path):
            with open(pth_path, "r", encoding="utf-8") as f:
                if module_dir in f.read():
                    print(f"이미 등록되어 있습니다: {pth_path}")
                    return True

        with open(pth_path, "w", encoding="utf-8") as f:
            f.write(module_dir + "\n")

        print(f"'{module_dir}' 를 import 가능하도록 등록했습니다.")
        print(f"(.pth 파일: {pth_path})")
        print(f"적용된 python: {sys.executable}")
        return True
    except PermissionError:
        print(f"Error: 쓰기 권한이 없습니다: {pth_path}")
        print("관리자 권한(sudo) 없이 사용자 site-packages에 설치되도록 venv 사용을 권장합니다.")
        return False
    except Exception as e:
        print(f"Error: .pth 등록 실패: {e}")
        return False


# ── 추가: VSCode에서 import 빨간줄(오류 표시) 안 뜨게 자동 등록 ──────
def get_vscode_settings_paths():
    """
    VSCode(및 Insiders) 전역 User settings.json 경로 후보를 OS별로 반환한다.
    실제 설치되어 폴더가 존재하는 것만 대상으로 한다.
    """
    home_dir = os.path.expanduser("~")
    candidates = []

    if sys.platform == "darwin":
        base = os.path.join(home_dir, "Library", "Application Support")
        candidates = [
            os.path.join(base, "Code", "User", "settings.json"),
            os.path.join(base, "Code - Insiders", "User", "settings.json"),
        ]
    elif os.name == "nt":
        appdata = os.environ.get("APPDATA", os.path.join(home_dir, "AppData", "Roaming"))
        candidates = [
            os.path.join(appdata, "Code", "User", "settings.json"),
            os.path.join(appdata, "Code - Insiders", "User", "settings.json"),
        ]
    else:
        base = os.path.join(home_dir, ".config")
        candidates = [
            os.path.join(base, "Code", "User", "settings.json"),
            os.path.join(base, "Code - Insiders", "User", "settings.json"),
        ]

    # 부모 폴더(User)가 존재하는 것만 = VSCode가 실제로 설치/실행된 적 있는 경우
    return [p for p in candidates if os.path.isdir(os.path.dirname(p))]


def register_vscode_settings(module_dir: str) -> bool:
    """
    VSCode 전역 User settings.json 의 python.analysis.extraPaths 에
    module_dir 을 추가해서, 어떤 프로젝트를 열어도 Pylance가
    `import grpe_sdk` 를 오류로 표시하지 않도록 한다.
    - 기존 settings.json 내용은 보존하고 extraPaths 항목에만 추가한다.
    - VSCode가 설치되어 있지 않으면 조용히 건너뛴다 (실패로 취급하지 않음).
    """
    settings_paths = get_vscode_settings_paths()

    if not settings_paths:
        print("VSCode 설정 폴더를 찾지 못했습니다. (VSCode 미설치로 간주, 건너뜀)")
        return True

    any_success = False

    for settings_path in settings_paths:
        try:
            data = {}
            if os.path.exists(settings_path):
                with open(settings_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                if content:
                    try:
                        data = json.loads(content)
                    except json.JSONDecodeError:
                        print(f"Warning: {settings_path} 파싱 실패 (주석 포함 등). 수동으로 추가해주세요:")
                        print(f'  "python.analysis.extraPaths": ["{module_dir}"]')
                        continue

            extra_paths = data.get("python.analysis.extraPaths", [])
            if module_dir in extra_paths:
                print(f"이미 등록되어 있습니다: {settings_path}")
                any_success = True
                continue

            extra_paths.append(module_dir)
            data["python.analysis.extraPaths"] = extra_paths

            os.makedirs(os.path.dirname(settings_path), exist_ok=True)
            with open(settings_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print(f"VSCode 설정에 등록했습니다: {settings_path}")
            any_success = True
        except Exception as e:
            print(f"Warning: {settings_path} 등록 실패: {e}")

    return any_success


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
            script_dir = os.path.dirname(script_path)

            cli_success = register_script_runner(script_path, COMMAND_NAME)
            print()
            module_success = register_module_path(script_dir)
            print()
            register_vscode_settings(script_dir)

            if cli_success and module_success:
                print("\nSetup Success.")
                print(f"Execute '{COMMAND_NAME}' on terminal or cmd")
                print("Or use 'import grpe_sdk' in any python script.")

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
