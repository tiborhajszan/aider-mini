import sys, pyperclip
from mini.sys_prompt import copy_sys_prompt

def main():

  print("\n[✓] Aider Mini CLI initialized.")
  print("Type a command (e.g., /sys) or /quit to exit.\n")

  while True:

    try:

      # read
      user_input = input("mini> ").strip()

      # skip empty inputs
      if not user_input:
        continue

      # /quit
      if user_input.lower() in ["/quit", "/q", "/exit", "exit"]:
        print("Exiting Aider Mini. Goodbye!")
        sys.exit(0)

      # /sys
      elif user_input == "/sys":
        if copy_sys_prompt():
          clipboard_content = pyperclip.paste()
          print("\n[ --- CURRENT CLIPBOARD CONTENT --- ]")
          print(clipboard_content)
          print("[ --- END OF CLIPBOARD --- ]\n")
        else:
          print("[!] sys_prompt failed.")

      # handling unknown command
      else:
        print(f"[?] Unknown command: '{user_input}'. Available commands: /sys, /quit")

    except (KeyboardInterrupt, EOFError):

      print("\nExiting Aider Mini. Goodbye!")
      sys.exit(0)

if __name__ == "__main__":
  main()
