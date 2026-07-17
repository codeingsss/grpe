import pyfiglet
# --- 글자 색상 (Foreground) ---
BLACK   = "\033[30m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"

# --- 밝은 글자 색상 (Bright Foreground) ---
BRIGHT_BLACK   = "\033[90m"
BRIGHT_RED     = "\033[91m"
BRIGHT_GREEN   = "\033[92m"
BRIGHT_YELLOW  = "\033[93m"
BRIGHT_BLUE    = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN    = "\033[96m"
BRIGHT_WHITE   = "\033[97m"

# --- 배경 색상 (Background) ---
BG_BLACK   = "\033[40m"
BG_RED     = "\033[41m"
BG_GREEN   = "\033[42m"
BG_YELLOW  = "\033[43m"
BG_BLUE    = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN    = "\033[46m"
BG_WHITE   = "\033[47m"

RESET = "\033[0m"


def bnr():
    ascii_art = pyfiglet.figlet_format(f"GRPE", font="standard")
    print(f"{GREEN}{ascii_art}{RESET}")

def cstm(text,fot,color):
    ascii_art = pyfiglet.figlet_format(f"{text}", font=fot)
    print(f"{color}{ascii_art}{RESET}")