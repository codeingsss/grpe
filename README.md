# GRPE

GRPE is a Python-based AI command-line tool that turns natural language instructions into executable shell commands using Gemini.

## Project Structure

- SDK
  - Contains the core Python SDK used by the shell versions.
- v1 shell
  - An interactive terminal shell that runs locally and stores the API key in a local file.
- v2 shell
  - A more complete shell experience with an installer and command registration support.

## Requirements

- Python 3.8 or newer
- pyfiglet
- google-genai

Install the required packages with:

```bash
pip install pyfiglet google-genai
```

## Usage Overview

1. Choose the version you want to use:
   - v1 shell for a simple interactive experience
   - v2 shell for a more complete setup experience
2. Follow the instructions in the relevant folder's README.
3. Provide a Gemini API key when prompted.
4. Start entering commands in natural language.

## Notes

- The project uses Gemini to generate shell commands from prompts.
- Commands are executed in the environment where the script is running.
- The SDK and shell versions are intended for practical command generation and local automation workflows.
