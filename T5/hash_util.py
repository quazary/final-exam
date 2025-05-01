import hashlib
import json
import sys
import os

HASH_FILE = "hashes.json"

def compute_hashes(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    return {
        "md5": hashlib.md5(data).hexdigest(),
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }

def save_hashes(hashes, filename):
    with open(filename, "w") as f:
        json.dump(hashes, f, indent=4)
    print(f"[+] Hashes saved to {filename}")

def load_hashes(filename):
    with open(filename, "r") as f:
        return json.load(f)

def check_integrity(reference, current):
    passed = True
    for algo in reference:
        if reference[algo] != current[algo]:
            print(f"[!] {algo.upper()} mismatch!")
            print(f"    Expected: {reference[algo]}")
            print(f"    Found:    {current[algo]}")
            passed = False
    if passed:
        print("[✓] Integrity check passed.")
    else:
        print("[✗] Integrity check failed.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:")
        print("  Save hashes:    python hash_util.py save original.txt")
        print("  Check file:     python hash_util.py check tampered.txt")
        sys.exit(1)

    command = sys.argv[1]
    target_file = sys.argv[2]

    if not os.path.exists(target_file):
        print(f"[!] File not found: {target_file}")
        sys.exit(1)

    if command == "save":
        hashes = compute_hashes(target_file)
        save_hashes(hashes, HASH_FILE)
    elif command == "check":
        reference = load_hashes(HASH_FILE)
        current = compute_hashes(target_file)
        check_integrity(reference, current)
    else:
        print("[!] Unknown command. Use 'save' or 'check'.")
