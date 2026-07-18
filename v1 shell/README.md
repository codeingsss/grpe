# GRPE v1 Shell

This folder contains the first version of the GRPE shell experience.

## Features

- Interactive prompt-based command execution
- Gemini-powered command generation
- Local API key storage in api.grpe

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
2. Run the main script:

```bash
python main.py
```

3. When prompted, enter your Gemini API key.
4. Start typing natural language commands.

## Using the SDK in Your Own Project

You can also use the CLI helper module in your own project:

1. Copy v1 shell/grpe_cli.py into your project folder.
2. Import grpe_cli.
3. Use the cli() function to generate and execute commands from text prompts.
