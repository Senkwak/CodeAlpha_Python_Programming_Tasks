# ============================================================
#  TASK 3 — TASK AUTOMATION WITH PYTHON SCRIPTS
#  CodeAlpha Python Internship
#  Concepts: os, shutil, re, requests, file handling
#
#  3 options available (menu at launch):
#    A) Move .jpg files to a new folder
#    B) Extract email addresses from a .txt file
#    C) Scrape the title of a fixed webpage
# ============================================================

import os
import shutil
import re
import sys

# ── Optional import of requests ──────────────────────────────
# Import requests only if available; set flag accordingly
try:
    import requests  # type: ignore
    REQUESTS_OK = True
except Exception:
    # If requests is not installed or cannot be imported in this environment,
    # ensure the rest of the script can still run.
    REQUESTS_OK = False



#   OPTION A — Move .jpg files                             


def move_jpg_files(source_folder: str, target_folder: str) -> None:
    """
    Moves all .jpg (and .jpeg) files from the source folder
    to the target folder (created automatically if it doesn't exist).
    """
    # Check that the source folder exists
    if not os.path.isdir(source_folder):
        print(f"   Source folder not found: {source_folder}")
        return

    # Create target folder if needed
    os.makedirs(target_folder, exist_ok=True)

    # List .jpg / .jpeg files
    jpg_files = [
        f for f in os.listdir(source_folder)
        if f.lower().endswith((".jpg", ".jpeg"))
        and os.path.isfile(os.path.join(source_folder, f))
    ]

    if not jpg_files:
        print(" No .jpg files found in the source folder.")
        return

    print(f"\n {len(jpg_files)} .jpg file(s) found:\n")
    moved   = 0
    skipped = 0

    for name in jpg_files:
        src  = os.path.join(source_folder, name)
        dest = os.path.join(target_folder, name)

        # Handle filename conflicts
        if os.path.exists(dest):
            base, ext = os.path.splitext(name)
            counter = 1
            while os.path.exists(dest):
                dest = os.path.join(target_folder, f"{base}_{counter}{ext}")
                counter += 1
            print(f"    Conflict: {name} → renamed to {os.path.basename(dest)}")

        shutil.move(src, dest)
        print(f"   Moved: {name}")
        moved += 1

    print(f"\n   Result: {moved} moved, {skipped} skipped")
    print(f"   Target folder: {os.path.abspath(target_folder)}\n")


#   OPTION B — Extract email addresses                     

# Regex pattern to detect email addresses
EMAIL_REGEX = re.compile(
    r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
)


def extract_emails(input_file: str, output_file: str) -> None:
    """
    Reads a .txt file, extracts all unique email addresses
    and saves them to an output file.
    """
    if not os.path.isfile(input_file):
        print(f"   File not found: {input_file}")
        return

    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Extract with regex — set() removes duplicates
    found_emails = sorted(set(EMAIL_REGEX.findall(content)))

    if not found_emails:
        print("    No email addresses found in the file.")
        return

    print(f"\n  {len(found_emails)} email address(es) found:\n")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Email addresses extracted from: {input_file}\n")
        f.write(f"Total count: {len(found_emails)}\n")
        f.write("=" * 50 + "\n\n")
        for email in found_emails:
            f.write(email + "\n")
            print(f"  • {email}")

    print(f"\n   Emails saved to: {os.path.abspath(output_file)}\n")


#   OPTION C — Scrape the title of a webpage               

def extract_html_title(html: str) -> str:
    """
    Extracts the content of the <title> tag from an HTML string.
    Uses a simple regex (no BeautifulSoup required).
    """
    match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if match:
        # Clean up extra whitespace and line breaks
        return re.sub(r"\s+", " ", match.group(1)).strip()
    return "(Title not found)"


def scrape_title(url: str, output_file: str) -> None:
    """
    Makes a GET request to the given URL, extracts the HTML page
    title and saves it to a text file.
    """
    if not REQUESTS_OK:
        print("   The 'requests' module is not installed.")
        print("     Run: pip install requests")
        return

    print(f"\n    Connecting to: {url}")

    try:
        response = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (CodeAlpha-Bot/1.0)"
        })
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print(" Connection error. Check your internet access.")
        return
    except requests.exceptions.Timeout:
        print(" Request timed out.")
        return
    except requests.exceptions.HTTPError as e:
        print(f"  HTTP error: {e}")
        return

    title = extract_html_title(response.text)
    print(f"  Title found: {title}")

    # Save to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"URL    : {url}\n")
        f.write(f"Title  : {title}\n")
        f.write(f"Status : {response.status_code} {response.reason}\n")

    print(f" Title saved to: {os.path.abspath(output_file)}\n")


#   MAIN MENU                                              

def menu():
    print("=" * 52)
    print("     TASK AUTOMATION — CodeAlpha")
    print("=" * 52)
    print("  Choose an option:\n")
    print("  [A] Move .jpg files to a target folder")
    print("  [B] Extract emails from a .txt file")
    print("  [C] Scrape the title of a webpage")
    print("  [Q] Quit")
    print()
    return input("  Your choice: ").strip().upper()


def main():
    choice = menu()

    # Option A 
    if choice == "A":
        print("\n   MOVING .JPG FILES\n")
        source = input("  Source folder (e.g. C:/Images)       : ").strip()
        target = input("  Target folder (e.g. C:/Images/JPG)   : ").strip()
        move_jpg_files(source, target)

    #  Option B 
    elif choice == "B":
        print("\n   EXTRACTING EMAIL ADDRESSES\n")
        input_f  = input("  Source .txt file (e.g. contacts.txt) : ").strip()
        output_f = input("  Output file      (e.g. emails.txt)   : ").strip()
        extract_emails(input_f, output_f)

    #  Option C 
    elif choice == "C":
        print("\n   SCRAPING A WEBPAGE TITLE\n")
        url      = input("  Page URL    (e.g. https://example.com) : ").strip()
        output_f = input("  Output file (e.g. title.txt)           : ").strip()
        scrape_title(url, output_f)

    #  Quit 
    elif choice == "Q":
        print("\n   Goodbye!\n")
        sys.exit(0)

    else:
        print("\n    Invalid option. Please restart the program.\n")


if __name__ == "__main__":
    main()