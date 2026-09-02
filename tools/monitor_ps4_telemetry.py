#!/usr/bin/env python3
r"""
tools/monitor_ps4_telemetry.py
==============================
Live PS4 GoldHEN KLog & Mod Telemetry Monitoring Suite for GoldSantos.
Captures kernel ring buffer output, game lifecycle events, PRX hooks, and crashes.

Features:
- Automatic local log persistence to logs/ps4_telemetry_YYYYMMDD_HHMMSS.log and logs/ps4_telemetry_latest.log.
- ANSI color-coded console streaming with real-time categorizations ([CRITICAL/CRASH], [PLUGIN/HOOK], [GAME/EXEC], [WARN]).
- Clean, non-colored, ISO-timestamped disk logging for post-mortem forensics.
- Live daemon health check (--check) for KLog (3232), Cheat Server (2801), and FTP (21/2121).
- Automatic reconnection on socket drop or game reboot.
"""

import os
import sys
import time
import socket
import argparse
import re
from datetime import datetime
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = ROOT_DIR / "logs"

# Default configuration from environment
PS4_IP = os.environ.get("PS4_IP", "192.168.1.100")
KLOG_PORT = 3232
CHEAT_PORT = 2801
FTP_PORTS = [2121, 21]

# ANSI Color codes
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
DIM = "\033[90m"

ANSI_STRIP_REGEX = re.compile(r'\x1b\[[0-9;]*m')

def strip_ansi(text: str) -> str:
    return ANSI_STRIP_REGEX.sub('', text)

def probe_port(ip: str, port: int, timeout: float = 2.0) -> bool:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        res = s.connect_ex((ip, port))
        s.close()
        return res == 0
    except Exception:
        return False

def check_ps4_status(ip: str):
    print("=" * 75)
    print(f" {BOLD}GoldSantos PS4 Diagnostics & Telemetry Service Health Check{RESET}")
    print(f" Target Console: {CYAN}{ip}{RESET}")
    print("=" * 75)

    # 1. KLog Server (Port 3232)
    klog_ok = probe_port(ip, KLOG_PORT)
    status_klog = f"{GREEN}ONLINE{RESET}" if klog_ok else f"{RED}OFFLINE (Enable in GoldHEN -> Klog Settings){RESET}"
    print(f"  • KLog Server (Port {KLOG_PORT}):        {status_klog}")

    # 2. Cheat Server (Port 2801)
    cheat_ok = probe_port(ip, CHEAT_PORT)
    status_cheat = f"{GREEN}ONLINE{RESET}" if cheat_ok else f"{YELLOW}IDLE / CLOSED (Active during game or via Settings){RESET}"
    print(f"  • Cheat Server (Port {CHEAT_PORT}):       {status_cheat}")

    # 3. FTP Server (Port 2121 or 21)
    ftp_active_port = None
    for p in FTP_PORTS:
        if probe_port(ip, p):
            ftp_active_port = p
            break
    status_ftp = f"{GREEN}ONLINE (Port {ftp_active_port}){RESET}" if ftp_active_port else f"{RED}OFFLINE (Enable in GoldHEN -> FTP Server){RESET}"
    print(f"  • FTP Server (Ports 2121/21):      {status_ftp}")

    print("-" * 75)
    if klog_ok:
        print(f"{GREEN}{BOLD}[READY]{RESET} KLog Server is active and ready to stream real-time logs!")
    else:
        print(f"{YELLOW}{BOLD}[ACTION REQUIRED]{RESET} To stream live kernel logs:")
        print("  1. On PS4, open: Settings -> GoldHEN -> Klog Settings.")
        print("  2. Toggle 'Enable Klog Server' to ON.")
        print("  3. (Optional) Toggle 'TTY Redirect' to ON.")
    print("=" * 75)
    return klog_ok

def format_line(line: str) -> tuple[str, str]:
    """Format and syntax-highlight klog output; returns (colored_console, clean_log)."""
    now = datetime.now()
    timestamp_short = now.strftime("%H:%M:%S")
    timestamp_iso = now.isoformat()
    clean = line.strip()

    if not clean:
        return "", ""

    prefix_console = f"{DIM}[{timestamp_short}]{RESET}"
    category = "INFO"

    # Critical errors & crashes
    if any(k in clean.lower() for k in ["panic", "fatal", "fault", "trap", "page fault", "sigsegv", "sigbus", "ce-34878"]):
        category = "CRITICAL/CRASH"
        colored = f"{prefix_console} {RED}{BOLD}[CRITICAL/CRASH]{RESET} {RED}{clean}{RESET}"
    # GoldHEN & Plugins
    elif any(k in clean for k in ["GoldHEN", "game_patch", "afr", "plugin", "PRX", "lotus", "menu", "patch"]):
        category = "PLUGIN/HOOK"
        colored = f"{prefix_console} {CYAN}{BOLD}[PLUGIN/HOOK]{RESET} {CYAN}{clean}{RESET}"
    # Game and Process Lifecycle
    elif any(k in clean for k in ["CUSA00411", "eboot.bin", "process", "kill", "exit", "launch"]):
        category = "GAME/EXEC"
        colored = f"{prefix_console} {GREEN}{BOLD}[GAME/EXEC]{RESET} {GREEN}{clean}{RESET}"
    # Warnings & Memory anomalies
    elif any(k in clean.lower() for k in ["warn", "fail", "error", "drop", "refused", "denied"]):
        category = "WARN"
        colored = f"{prefix_console} {YELLOW}[WARN]{RESET} {YELLOW}{clean}{RESET}"
    else:
        colored = f"{prefix_console} {clean}"

    log_entry = f"[{timestamp_iso}] [{category}] {clean}"
    return colored, log_entry

def stream_klog(ip: str, port: int, output_file: str = None):
    # Ensure logs directory exists
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    session_ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    if not output_file:
        session_log_path = LOGS_DIR / f"ps4_telemetry_{session_ts}.log"
    else:
        session_log_path = Path(output_file)

    latest_log_path = LOGS_DIR / "ps4_telemetry_latest.log"

    print("=" * 75)
    print(f" {BOLD}GoldSantos Live PS4 Telemetry & Kernel Log Monitor{RESET}")
    print(f" Target: {CYAN}{ip}:{port}{RESET}")
    print(f" Session Log: {GREEN}{session_log_path.relative_to(ROOT_DIR) if session_log_path.is_relative_to(ROOT_DIR) else session_log_path}{RESET}")
    print(f" Latest Symlink/Copy: {GREEN}logs/ps4_telemetry_latest.log{RESET}")
    print("=" * 75)

    if not probe_port(ip, port):
        print(f"\n{YELLOW}{BOLD}[i] KLog Server is currently offline at {ip}:{port}.{RESET}")
        print("Waiting for KLog server to become active...")
        print("  -> Please ensure GoldHEN is loaded and 'Enable Klog Server' is ON in Settings.")
        print("-" * 75)
        retry_count = 0
        while not probe_port(ip, port):
            time.sleep(2)
            retry_count += 1
            if retry_count % 10 == 0:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Still listening for {ip}:{port}...")

    print(f"\n{GREEN}✔ KLog Server online! Connecting to {ip}:{port}...{RESET}\n")

    f_session = open(session_log_path, "a", encoding="utf-8")
    f_latest = open(latest_log_path, "w", encoding="utf-8")

    header = f"=== GoldSantos PS4 Telemetry Session Started: {datetime.now().isoformat()} ===\nTarget: {ip}:{port}\n\n"
    f_session.write(header)
    f_latest.write(header)
    f_session.flush()
    f_latest.flush()

    line_count = 0
    crash_count = 0

    try:
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, port))
                sock.settimeout(None)
                print(f"{GREEN}[CONNECTED] Live stream active. Intercepting game events & kernel logs...{RESET}\n")

                buffer = ""
                while True:
                    data = sock.recv(4096)
                    if not data:
                        print(f"\n{YELLOW}[DISCONNECTED] Server closed socket. Reconnecting...{RESET}")
                        break

                    buffer += data.decode("utf-8", errors="replace")
                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        colored, plain = format_line(line)
                        if colored:
                            print(colored)
                            line_count += 1
                            if "CRITICAL/CRASH" in plain:
                                crash_count += 1
                            f_session.write(plain + "\n")
                            f_latest.write(plain + "\n")
                            f_session.flush()
                            f_latest.flush()

            except (socket.error, ConnectionResetError) as e:
                print(f"{YELLOW}[CONNECTION LOST] {e}. Reconnecting in 3 seconds...{RESET}")
                time.sleep(3)

    except KeyboardInterrupt:
        print(f"\n{CYAN}Monitor session stopped by user.{RESET}")
    finally:
        footer = f"\n=== GoldSantos Telemetry Session Finished: {datetime.now().isoformat()} (Lines: {line_count}, Crashes: {crash_count}) ===\n"
        f_session.write(footer)
        f_latest.write(footer)
        f_session.close()
        f_latest.close()
        print(f"[+] Complete session log saved to: {session_log_path}")

def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Live PS4 GoldHEN KLog & Mod Telemetry Monitor")
    parser.add_argument("--ip", default=PS4_IP, help=f"PS4 IP address (default: {PS4_IP} or env PS4_IP)")
    parser.add_argument("--port", type=int, default=KLOG_PORT, help=f"Klog port (default: {KLOG_PORT})")
    parser.add_argument("--output", "-o", default=None, help="Custom output log file path (defaults to logs/ps4_telemetry_<timestamp>.log)")
    parser.add_argument("--check", action="store_true", help="Perform non-blocking status check on PS4 telemetry services and exit")

    args = parser.parse_args()

    if args.check:
        check_ps4_status(args.ip)
    else:
        stream_klog(args.ip, args.port, args.output)

if __name__ == "__main__":
    main()
