#!/usr/bin/env python3
import os
import sys
import time
import subprocess

OUTPUT_DIR = os.path.expanduser("~/Desktop")
OUTPUT_BASENAME = "copy_log"
POLL_INTERVAL = 1.0
SEPARATOR = "\n\n"
LABEL_MODE = len(sys.argv) > 1
LABELS = ["---\n\nUser:", "---\n\nAssistant:"]

def get_output_file():
    counter = 1
    while True:
        candidate = os.path.join(OUTPUT_DIR, f"{OUTPUT_BASENAME}_{counter}.txt")
        if not os.path.exists(candidate):
            return candidate
        counter += 1

def get_clipboard():
    result = subprocess.run( ["xclip", "-selection", "clipboard", "-o"], capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout

def normalize(text):
    lines = text.splitlines()
    lines = [line for line in lines if line.strip() != ""]
    return "\n".join(lines).strip()

def append_to_file(output_file, text, label_index):
    file_exists = os.path.exists(output_file)
    with open(output_file, "a", encoding="utf-8") as f:
        if file_exists and os.path.getsize(output_file) > 0:
            f.write(SEPARATOR)
        if LABEL_MODE:
            f.write(LABELS[label_index] + "\n")
        f.write(text)

def watch_clipboard():
    output_file = get_output_file()
    print(f"Watching clipboard, appending to {output_file}.")
    if LABEL_MODE:
        print("Label mode on.")
    print("Press Ctrl+C to stop.")
    last_content = normalize(get_clipboard() or "")
    label_index = 0
    while True:
        time.sleep(POLL_INTERVAL)
        current_raw = get_clipboard()
        if current_raw is None:
            continue
        current = normalize(current_raw)
        if current and current != last_content:
            append_to_file(output_file, current, label_index)
            print(f"Appended {len(current)} chars.")
            last_content = current
            label_index = 1 - label_index

def main():
    try:
        watch_clipboard()
    except KeyboardInterrupt:
        print("\nStopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()
