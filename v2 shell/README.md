# GRPE v2 Shell

This folder contains the second version of the GRPE shell experience, including an installer and a shell command entry point.

## Features

- Interactive shell usage
- Setup script for installing the command runner
- API key storage in the user's home directory
- Optional conversational mode by prefixing the prompt with (talkmod)

## Requirements

- Python 3.8 or newer
- pyfiglet
- google-genai

Install the dependencies with:

```bash
pip install pyfiglet google-genai
```

## How to Use

1. Open this folder in a terminal.
2. Run the installer:

```bash
python install.py
```

3. Follow the setup prompts to register the command and save your Gemini API key.
4. If you are on macOS, reload your shell configuration if required:

```bash
source ~/.zshrc
```

5. Run the command from the terminal:

```bash
grep e
```

If you want to use conversational-style output, add (talkmod) before your prompt.
