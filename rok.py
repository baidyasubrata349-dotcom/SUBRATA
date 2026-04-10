#!/usr/bin/env python3
"""
Final Animated One-Time Banner Version
- Banner animates once
- Below it shows "Send your target number"
- Results appear below (no re-animation)
- Clean colorful output only
"""

import os, sys, time, re, json, random, shutil
from urllib.parse import quote_plus
from datetime import datetime, timezone

try:
    import requests, urllib3
    from colorama import init, Fore, Style
except Exception:
    print("Install: pip install requests colorama")
    sys.exit(1)

# === CONFIG ===
API_BASE = "http://exploitsindia.site/anish/api.php?key=anish&num="
REQUEST_TIMEOUT = 20
VERIFY_SSL = False
GEN_SECONDS = 3

init(autoreset=True)
if not VERIFY_SSL:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# === Banner ===
BANNER = [
"               _   _ _____  _____ _    _     ________   _______  _      ____ _____ _______ _____  ",
"     /\\   | \\ | |_   _|/ ____| |  | |   |  ____\\ \\ / /  __ \\| |    / __ \\_   _|__   __/ ____| ",
"    /  \\  |  \\| | | | | (___ | |__| |   | |__   \\ V /| |__) | |   | |  | || |    | | | (___   ",
"   / /\\ \\ | . ` | | |  \\___ \\|  __  |   |  __|   > < |  ___/| |   | |  | || |    | |  \\___ \\  ",
"  / ____ \\| |\\  |_| |_ ____) | |  | |   | |____ / . \\| |    | |___| |__| || |_   | |  ____) | ",
" /_/    \\_\\_| \\_|_____|_____/|_|  |_|   |______/_/ \\_\\_|    |______\\____/_____|  |_| |_____/  "
]
WELCOME = "WELCOME SUBRATA"
PROMPT = "ð²  NUMBBER CHECK  ð²"

# === Helpers ===
def clear(): sys.stdout.write("\x1b[2J\x1b[H"); sys.stdout.flush()
def now_str(): return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
def term_size(): return shutil.get_terminal_size(fallback=(80, 24))
def height(): return term_size()[1]

# === Color Animation ===
def print_colored(text, delay=0.001):
    colors = [Fore.CYAN, Fore.YELLOW, Fore.LIGHTGREEN_EX, Fore.MAGENTA, Fore.LIGHTBLUE_EX]
    for line in text.splitlines():
        color = random.choice(colors)
        for c in line:
            print(color + c, end='', flush=True)
            time.sleep(delay)
        print()

def slide_banner_once():
    clear()
    rows = height() // 2
    banner_text = "\n".join(BANNER)
    for lead in range(rows, -1, -2):   # smooth slide
        clear()
        print("\n" * lead + Fore.CYAN + banner_text)
        time.sleep(0.01)
    print(Fore.YELLOW + "\n" + WELCOME)
    print(Fore.MAGENTA + PROMPT)
    print(Fore.WHITE + "\nEnter 10-digit number (or EXIT):\n")

def generating_animation(seconds=GEN_SECONDS):
    frames = ["[=     ]","[==    ]","[===   ]","[ ==== ]","[  === ]","[   == ]","[    = ]"]
    end = time.time() + seconds; i = 0
    while time.time() < end:
        sys.stdout.write("\rGenerating " + frames[i % len(frames)])
        sys.stdout.flush(); i += 1; time.sleep(0.18)
    sys.stdout.write("\r" + " " * 40 + "\r"); sys.stdout.flush()

# === API ===
def api_call(number):
    url = API_BASE + quote_plus(number)
    try:
        r = requests.get(url, timeout=REQUEST_TIMEOUT, verify=VERIFY_SSL)
        r.raise_for_status()
        return r.text
    except Exception as e:
        raise RuntimeError(str(e))

def sanitize_text(s):
    if not isinstance(s, str): s = str(s)
    s = re.sub(r'"join_main".*?"[^"]+"', '"join_main":"https://t.me/ExploitsAbout"', s)
    return s.strip()

# === Show Result ===
def show_result(parsed, number):
    print(Fore.CYAN + f"\nð Results for {number}\n")
    if isinstance(parsed, dict) and "data" in parsed and isinstance(parsed["data"], list):
        data = parsed["data"]
        if not data:
            print(Fore.RED + "â ï¸ No result found.")
            return
        for idx, d in enumerate(data, 1):
            print(Fore.LIGHTRED_EX + f"\n=== [ RESULT {idx} ] ===")
            print_colored(json.dumps(d, indent=2, ensure_ascii=False))
    else:
        print_colored(json.dumps(parsed, indent=2, ensure_ascii=False))

    print(Fore.RED + "\nâ¡ Made by ANISH EXPLOITS")
    print(Fore.BLUE + "ð Join: https://t.me/ExploitsAbout\n")

# === Main ===
def main():
    slide_banner_once()

    while True:
        try:
            num = input(Fore.CYAN + "> ").strip()
        except KeyboardInterrupt:
            print("\nExiting...")
            break

        if not num: continue
        if num.lower() in ["exit", "quit"]: break
        if not re.match(r"^\d{10}$", num):
            print(Fore.RED + "â Invalid number, enter exactly 10 digits.")
            continue

        print(f"\n{now_str()}  ð Processing your request...")
        generating_animation()

        try:
            raw = api_call(num)
        except Exception as e:
            print(Fore.RED + f"â API error: {e}")
            continue

        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = {"data": [sanitize_text(raw)]}

        print()  # no clear(), keep banner visible
        show_result(parsed, num)

        print(Fore.YELLOW + "\n--- END ---")
        print("Enter another number or type EXIT.\n")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        print("\nExited.")
