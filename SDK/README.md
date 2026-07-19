# GRPE SDK

This folder contains a lightweight Python SDK for sending natural language instructions to Gemini and executing the resulting shell command locally.

## Files

- grpe_sdk.py
  - Main SDK module.
  - Provides set_api(), ask_gemini(), and grpe().
  - Sends a prompt to Gemini with the current operating system and command history, then runs the generated command through the shell.

- color.py
  - Defines ANSI escape sequences for terminal text colors.
  - This file is used for console styling and does not contain the main SDK logic.

- setup_sdk.py
  - Registers the SDK script so it can be launched from the terminal as a command.
  - On macOS and Linux, it creates a launcher in ~/.local/bin.
  - On Windows, it creates a launcher in a user-level bin directory and updates PATH.

## Requirements

- Python 3.8 or newer
- google-genai
- pyfiglet (optional, used by the setup banner)

Install the required packages with:

```bash
pip install google-genai pyfiglet
```

## Basic Usage

```python
import grpe_sdk

grpe_sdk.set_api("YOUR_GEMINI_API_KEY")

output = grpe_sdk.grpe("list files in the current directory")
print(output)
```

## Setup the Command Runner

To make the SDK available as a terminal command, run:

```bash
python setup_sdk.py
```

Then select option 1 to register the command. After setup, you can run:

```bash
grep e
```

If the shell does not recognize the command immediately, open a new terminal or reload the shell configuration.

## How It Works

1. The SDK stores your Gemini API key using set_api().
2. The grpe() function builds a prompt that includes the current operating system and previous command history.
3. Gemini returns a command string.
4. The SDK executes that command with subprocess and returns the standard output.

## Notes

- The generated command is executed through the shell, so it depends on the environment where the script is running.
- If the model cannot produce a valid command, the function will return None or print an error message.
- This SDK is intended for simple command-generation and local automation workflows rather than full production-grade automation.
