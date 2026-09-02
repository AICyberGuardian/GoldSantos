r"""
tools/audit_privacy_and_secrets.py
==================================
Automated privacy, path portability, and secrets auditing tool for GoldSantos.
Runs locally before commits or on demand to guarantee zero personal data leaks.

Checks:
1. Hardcoded absolute Windows/Unix filesystem paths (e.g. E:\, C:\Users, /home/)
2. Personal usernames and machine names
3. Specific private LAN IP addresses (allows standard RFC 1918 placeholder 192.168.1.100)
4. API keys, access tokens (ghp_, sk-, AKIA), and private keys
"""

import sys
import os
import re
import subprocess
from pathlib import Path

# Paths to scan
ROOT_DIR = Path(__file__).resolve().parent.parent

# Forbidden patterns
PATTERNS = [
    # 1. Drive paths (e.g. E:\, C:\, D:\)
    (re.compile(r'\b[A-Za-z]:\\[a-zA-Z0-9_\\-]+'), "Hardcoded Windows drive path"),
    # 2. Local user home directories
    (re.compile(r'(?:/Users/|\\Users\\|/home/)[a-zA-Z0-9_\\-]+', re.IGNORECASE), "User home directory path"),
    # 3. Personal username
    (re.compile(r'\bnyxar\b', re.IGNORECASE), "Personal username reference"),
    # 4. Specific private subnet IP (e.g. 192.168.99.x)
    (re.compile(r'\b192\.168\.99\.\d{1,3}\b'), "Private console LAN IP (192.168.99.x)"),
    # 5. Secrets and tokens
    (re.compile(r'\b(?:ghp_[a-zA-Z0-9]{20,}|gho_[a-zA-Z0-9]{20,}|github_pat_[a-zA-Z0-9_]{20,})\b'), "GitHub Personal Access Token"),
    (re.compile(r'\bsk-[a-zA-Z0-9]{20,}\b'), "OpenAI / Cloud Secret Key"),
    (re.compile(r'\bAKIA[0-9A-Z]{16}\b'), "AWS Access Key ID"),
    (re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'), "Private Key Header"),
]

# Ignored files (e.g. git internal files or this audit script itself)
IGNORED_FILES = {
    Path("tools/audit_privacy_and_secrets.py"),
    Path(".gitignore"),
}

def get_files_to_check(staged_only=False):
    try:
        if staged_only:
            cmd = ["git", "-C", str(ROOT_DIR), "diff", "--cached", "--name-only", "--diff-filter=ACM"]
        else:
            cmd = ["git", "-C", str(ROOT_DIR), "ls-files"]
        output = subprocess.check_output(cmd, text=True).splitlines()
        return [Path(p) for p in output if p.strip()]
    except Exception as e:
        print(f"[!] Warning: Git query failed ({e}). Scanning filesystem directly.")
        files = []
        for root, _, filenames in os.walk(ROOT_DIR):
            if ".git" in root or "__pycache__" in root:
                continue
            for f in filenames:
                rel = Path(root, f).relative_to(ROOT_DIR)
                files.append(rel)
        return files

def audit(staged_only=False):
    files = get_files_to_check(staged_only=staged_only)
    violations = []

    for rel_path in files:
        if rel_path in IGNORED_FILES:
            continue
        full_path = ROOT_DIR / rel_path
        if not full_path.is_file():
            continue

        try:
            content = full_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        for line_no, line in enumerate(content.splitlines(), 1):
            for regex, description in PATTERNS:
                matches = regex.findall(line)
                if matches:
                    violations.append((rel_path, line_no, description, matches, line.strip()))

    return violations

def main():
    staged_only = "--staged" in sys.argv
    mode_str = "staged changes" if staged_only else "all tracked files"
    print(f"[*] Running GoldSantos Privacy & Secrets Audit on {mode_str}...")

    violations = audit(staged_only=staged_only)

    if violations:
        print("\n" + "=" * 80)
        print("  [!] SECURITY / PRIVACY VIOLATIONS DETECTED - COMMIT REJECTED")
        print("=" * 80)
        for rel_path, line_no, desc, matches, line in violations:
            print(f"\n[-] {rel_path}:{line_no}")
            print(f"    Issue: {desc}")
            print(f"    Matched: {matches}")
            print(f"    Line: {line[:100]}")
        print("\n" + "=" * 80)
        print("Please fix the above violations before committing or pushing.")
        print("=" * 80)
        sys.exit(1)
    else:
        print("[+] Privacy & Secrets Audit PASSED! Zero personal data, paths, or secrets detected.")
        sys.exit(0)

if __name__ == "__main__":
    main()
