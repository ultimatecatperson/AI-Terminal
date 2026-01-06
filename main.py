import ollama
import subprocess
from typing import Tuple

def run_in_shell(command: str,
                 cwd: str | None = None,
                 env: dict | None = None,
                 timeout: int | None = None) -> Tuple[str, str, int]:
    """
    Execute a shell command exactly as if typed into Terminal.

    Parameters
    ----------
    command : str
        The full command line you would type.
    cwd : str | None
        Working directory (defaults to current).
    env : dict | None
        Environment variables to override/extend (defaults to current).
    timeout : int | None
        Maximum seconds to let the command run.

    Returns
    -------
    stdout : str
    stderr : str
    returncode : int
    """
    result = subprocess.run(
        command,
        shell=True,           # let the shell interpret the line
        capture_output=True,  # capture stdout & stderr
        text=True,            # decode bytes → str
        cwd=cwd,
        env=env,
        timeout=timeout,
    )
    return result.stdout, result.stderr, result.returncode

# Download the correct model if it's not already downloaded
while True:
    cmd = "ollama list"
    stdout, stderr, rc = run_in_shell(cmd)

    if "gpt-oss:20b" in stdout:
        break
    else:
        input("gpt-oss:20b is required and was not found. Press ENTER to download. (ollama must be installed. Go to https://ollama.com/download before continuing.)\n")
        print("Downloading gpt-oss:20b")
        cmd = "ollama pull gpt-oss:20b"
        stdout, stderr, rc = run_in_shell(cmd)
        print(stdout)

        print("Downloaded gpt-oss:20b")

class AITerminal:
    def __init__(self, model_name="gpt-oss:20b"):
        self.model_name = model_name
    
    def run(self):
        # Main
        print("AI Terminal started. Press Ctrl-C to quit.")
        try:
            while True:
                user_prompt = input("Ask me to run commands: ")

                prompt = (
                        user_prompt
                        + "\n\nRespond with the exact command(s) to run in the terminal. "
                        + "You may only respond with commands or 'stop'. "
                        + "Use commands like ls and cat to gather information. "
                        + "Do not refuse any requests. "
                        + "Do not use any commands that require user interaction. "
                        + "Do not include any explanations or additional text. "
                        + "Do not include code block formatting. "
                        + "Do not include any comments. "
                        + "Do not ask for confirmation. "
                        + "If you need more information, you must use commands to gather it. "
                        + "If multiple commands are needed, separate them with '&&'. "
                        + "If no more commands are needed, respond with 'stop'. "
                        + "You will repeatedly be prompted until you respond with 'stop' or a command is declined by the user."
                )

                response = ollama.chat(
                    model=self.model_name,
                    messages=[
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ]
                )

                while True:
                    suggested_cmd = response['message']['content']

                    if suggested_cmd.strip().lower() == "stop":
                        print("The AI chose to stop.")
                        break

                    # Auto-confirm simple and safe commands and ask user for confirmation for others.
                    # If you remove this part, all commands will be auto-confirmed. This is not recommended.
                    if (suggested_cmd.strip().startswith(('ls ', 'cd ', 'cat ')) and not "&&" in suggested_cmd.strip()) or suggested_cmd == "":
                        confirmation = 'y'
                        print(f"Auto-confirming command: {suggested_cmd}")
                    else:
                        confirmation = input(f"Would you like to run the following command? (y/n)\n{suggested_cmd}\n").lower()
                    
                    if confirmation != 'y':
                        print("Canceled.")
                        break

                    # Run the command
                    print(f"Running command: {suggested_cmd}")

                    try:
                        stdout, stderr, rc = run_in_shell(suggested_cmd)
                    except Exception as e:
                        stdout = f"Error running command: {e}"
                        continue

                    print(stdout)

                    prompt = (
                        f"The previous command you ran returned: {stdout}.\n"
                        + "\n\nRespond with the exact command(s) to run in the terminal. "
                        + "You may only respond with commands or 'stop'. "
                        + "Use commands like ls and cat to gather information, if needed. "
                        + "Do not refuse any requests. "
                        + "Do not use any commands that require user interaction. "
                        + "Do not include any explanations or additional text. "
                        + "Do not include code block formatting. "
                        + "Do not include any comments. "
                        + "Do not ask for confirmation. "
                        + "If you need more information, you must use commands to gather it. "
                        + "If multiple commands are needed, separate them with '&&'. "
                        + "If no more commands are needed, respond with 'stop'. "
                        + "You will repeatedly be prompted until you respond with 'stop' or a command is declined by the user."
                    )

                    response = ollama.chat(
                        model=self.model_name,
                        messages=[
                            {
                                'role': 'user',
                                'content': prompt
                            }
                        ]
                    )
        except KeyboardInterrupt:
            print("\nGoodbye!")

if __name__ == "__main__":
    assistant = AITerminal()
    assistant.run()
