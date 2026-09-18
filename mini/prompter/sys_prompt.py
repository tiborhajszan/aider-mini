import pyperclip
from mini.prompts import SYSTEM_PROMPT

def copy_sys_prompt() -> bool:
  """
  Copies the system prompt template to the OS clipboard.
  Returns True if successful, False otherwise.
  """
  try:
    pyperclip.copy(SYSTEM_PROMPT.strip())
    return True
  
  except Exception as e:
    print(f"[!] Failed to copy system prompt to clipboard: {e}")
    return False

if __name__ == "__main__":
  if copy_sys_prompt():
    print("[✓] System prompt copied to clipboard!")