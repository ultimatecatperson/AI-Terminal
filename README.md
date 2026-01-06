# AI Terminal

**WARNING**: Running AI models locally uses a lot of RAM! Make sure your computer has enough before continuing, preferably 32+ GB. (It ran just fine on 48 GB RAM) If you have a MacBook Air, Chromebook, or anything lightweight like that, turn away while you can!
## Overview
AI Terminal is an AI Assistant that runs commands in the terminal. You can ask it things like, "Create a directory for python and go into it.", and it should run commands like mkdir and cd to get the job done.

## Features
- AI can run any command inside your own Terminal
- User confirmation is always requested for commands other than ls, cat, and cd before running.
- AI will be able to keep controlling the terminal from its previous command running.

## Setup

1. **Prerequisites**  
    - Python 3.9+  
    - `pip` package manager
    - Ollama ([Download here](https://ollama.com/download))

2. **Clone the repository**  
    ```bash
    git clone https://github.com/ultimatecatperson/AI-Terminal
    cd AI_Terminal
    ```

3. **Create a virtual environment**  
    ```bash
    python -m venv .venv
    source .venv/bin/activate   # On Windows use `.venv\Scripts\activate`
    ```

4. **Install dependencies**  
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the assistant**  
    ```bash
    python main.py
    ```

## Usage

Once running, type your prompt and press Enter. The assistant will run commands on your behalf. You can press Ctrl+C to exit anytime while running.

## Feedback

Feedback is more than welcome by creating new issues.

## License

MIT License

> **Note**: Some content in this README file was AI-generated.