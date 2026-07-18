import os
import sys
import subprocess
import ctypes

def is_admin():
    try:
        if os.name == 'nt':
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.getuid() == 0
    except:
        return False

def register_script_runner(target_path):
    if not os.path.exists(target_path):
        return False

    target_path = os.path.abspath(target_path)

    if os.name == 'nt':
        if not is_admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()

        target_dir = target_path if os.path.isdir(target_path) else os.path.dirname(target_path)

        current_pathext = os.environ.get('PATHEXT', '')
        if '.PY' not in current_pathext.upper():
            new_pathext = f"{current_pathext};.PY;.PYW"
            subprocess.run(['setx', 'PATHEXT', new_pathext, '/M'], capture_output=True)

        try:
            subprocess.run('assoc .py=Python.File', shell=True, check=True, capture_output=True)
            py_path = sys.executable
            ftype_cmd = f'ftype Python.File="{py_path}" "%1" %*'
            subprocess.run(ftype_cmd, shell=True, check=True, capture_output=True)
        except subprocess.CalledProcessError:
            pass

        current_path = os.environ.get('PATH', '')
        if target_dir.lower() not in current_path.lower():
            subprocess.run(['setx', 'PATH', f"{current_path};{target_dir}", '/M'], capture_output=True)

    else:
        bin_dir = os.path.expanduser("~/.local/bin")
        os.makedirs(bin_dir, exist_ok=True)

        home = os.path.expanduser("~")
        shell = os.environ.get("SHELL", "")
        rc_file = os.path.join(home, ".zshrc") if "zsh" in shell else os.path.join(home, ".bashrc")

        # 수정: rc_file이 없어도 open(..., "a")가 자동으로 생성하도록 처리
        content = ""
        if os.path.exists(rc_file):
            with open(rc_file, "r") as f:
                content = f.read()

        if ".local/bin" not in content:
            with open(rc_file, "a") as f:
                f.write('\nexport PATH="$HOME/.local/bin:$PATH"\n')

        if os.path.isdir(target_path):
            for file in os.listdir(target_path):
                if file.endswith('.py'):
                    src = os.path.join(target_path, file)
                    dst = os.path.join(bin_dir, os.path.splitext(file)[0])
                    if os.path.exists(dst) or os.path.islink(dst):
                        os.remove(dst)
                    os.symlink(src, dst)
                    os.chmod(src, 0o755)
        elif os.path.isfile(target_path) and target_path.endswith('.py'):
            file_name = os.path.basename(target_path)
            dst = os.path.join(bin_dir, os.path.splitext(file_name)[0])
            if os.path.exists(dst) or os.path.islink(dst):
                os.remove(dst)
            os.symlink(target_path, dst)
            os.chmod(target_path, 0o755)
