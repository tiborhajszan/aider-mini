########################################################################################################################
### Aider Mini > Root > Command Loop
### Path: mini/cli.py
########################################################################################################################

import sys
import pyperclip
from mini.sys_prompt import copy_sys_prompt
from mini.editor.editor import run_editor

### main function ######################################################################################################
def main():
    """
    Aider Mini launch point and interactive CLI command loop.
    """

    ### terminal init --------------------------------------------------------------------------------------------------

    ### printing init message
    print("\n[✓] Aider Mini CLI initialized.")
    print("Type a command (e.g., /sys, /map, /apply) or /quit to exit.\n")

    ### command loop ---------------------------------------------------------------------------------------------------
    while True:

        #>> parsing/executing user input
        try:

            # reading user input | skipping empty inputs
            user_input: str = input("mini> ").strip()
            if not user_input:
                continue

            # /apply
            if user_input.startswith(("/apply", "/a")):
                command_parts: list[str] = user_input.split(maxsplit=1)
                target_path: str = command_parts[1].strip() if 1 < len(command_parts) else ""
                edit_response: dict = run_editor(target_path=target_path)
                if edit_response["status"] != 0:
                    print(f"\n{edit_response['message']}\n")
                else:
                    print(f"\n[✓] File Editor > Edit Applied to {target_path}\n")
                continue
            
            # /quit
            if user_input.lower() in ["/quit", "/q", "/exit"]:
                print("Exiting Aider Mini. Goodbye!\n")
                sys.exit(0)

            # /sys
            elif user_input == "/sys":
                if copy_sys_prompt():
                    clipboard_content = pyperclip.paste()
                    print("\n[ --- CURRENT CLIPBOARD CONTENT --- ]")
                    print(clipboard_content)
                    print("[ --- END OF CLIPBOARD --- ]\n")
                else:
                    print("[!] System Prompt generator failed.\n")

            # /map
            elif user_input == "/map":
                print("[!] /map command issued (repomap module pending implementation).\n")

            # handling unknown command
            else:
                print(f"[?] Unknown command: '{user_input}'. Available commands: /sys, /map, /quit\n")

        except (KeyboardInterrupt, EOFError):
            print("\nExiting Aider Mini. Goodbye!\n")
            sys.exit(0)

if __name__ == "__main__":
  main()
