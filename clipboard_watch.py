#!/usr/bin/env python3
import os
import sys
import time
import subprocess

OUTPUT_FILE = os.path.expanduser("~/Desktop/copy_log.txt")
POLL_INTERVAL = 2.0
SEPARATOR = "\n\n"

def get_clipboard():
    result = subprocess.run( ["xclip", "-selection", "clipboard", "-o"], capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout

def normalize(text):
    lines = text.splitlines()
    lines = [line for line in lines if line.strip() != ""]
    return "\n".join(lines).strip()

def append_to_file(text):
    file_exists = os.path.exists(OUTPUT_FILE)
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        if file_exists and os.path.getsize(OUTPUT_FILE) > 0:
            f.write(SEPARATOR)
        f.write(text)

def watch_clipboard():
    print(f"Watching clipboard, appending to {OUTPUT_FILE}.")
    print("Press Ctrl+C to stop.")
    last_content = normalize(get_clipboard() or "")
    while True:
        time.sleep(POLL_INTERVAL)
        current_raw = get_clipboard()
        if current_raw is None:
            continue
        current = normalize(current_raw)
        if current and current != last_content:
            append_to_file(current)
            print(f"Appended {len(current)} chars.")
            last_content = current

def main():
    try:
        watch_clipboard()
    except KeyboardInterrupt:
        print("\nStopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()
