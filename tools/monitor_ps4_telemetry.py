import socket
import sys
import time
import argparse
from datetime import datetime

import os

# Default configuration
PS4_IP = os.environ.get("PS4_IP", "192.168.1.100")
KLOG_PORT = 3232
FTP_PORT = 2121

# ANSI Color codes for readable console output
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
DIM = "\033[90m"

def format_line(line: str) -> str:
    """Format and syntax-highlight klog output based on content."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    clean = line.strip()
    
    if not clean:
        return ""

    prefix = f"{DIM}[{timestamp}]{RESET}"

    # Critical errors & crashes
    if any(k in clean.lower() for k in ["panic", "fatal", "fault", "trap", "page fault", "sigsegv", "sigbus", "ce-34878"]):
        return f"{prefix} {RED}{BOLD}[CRITICAL/CRASH]{RESET} {RED}{clean}{RESET}"
    
    # GoldHEN & Plugins
    elif any(k in clean for k in ["GoldHEN", "game_patch", "afr", "plugin", "PRX", "lotus", "menu"]):
        return f"{prefix} {CYAN}{BOLD}[PLUGIN/HOOK]{RESET} {CYAN}{clean}{RESET}"
    
    # Game and Process Lifecycle
    elif any(k in clean for k in ["CUSA00411", "eboot.bin", "process", "kill", "exit", "launch"]):
        return f"{prefix} {GREEN}{BOLD}[GAME/EXEC]{RESET} {GREEN}{clean}{RESET}"
    
    # Warnings & Memory anomalies
    elif any(k in clean.lower() for k in ["warn", "fail", "error", "drop", "refused", "denied"]):
        return f"{prefix} {YELLOW}[WARN]{RESET} {YELLOW}{clean}{RESET}"
    
    # Standard kernel log
    return f"{prefix} {clean}"

def probe_klog_server(ip: str, port: int, timeout: float = 3.0) -> bool:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        res = s.connect_ex((ip, port))
        s.close()
        return res == 0
    except Exception:
        return False

def stream_klog(ip: str, port: int, log_file: str = None):
    print("=" * 75)
    print(f" {BOLD}GoldSantos Live PS4 Telemetry & Kernel Log Monitor{RESET}")
    print(f" Target: {CYAN}{ip}:{port}{RESET} | Ready to intercept crashes, plugins & events")
    print("=" * 75)

    if not probe_klog_server(ip, port):
        print(f"\n{RED}{BOLD}[!] KLOG Server is NOT reachable at {ip}:{port}{RESET}")
        print("Please verify the following on your PS4:")
        print("  1. Console is powered on and GoldHEN v2.4b is loaded.")
        print("  2. In PS4: Settings -> GoldHEN -> Klog Settings:")
        print(f"     • {BOLD}Enable Klog Server: ON{RESET} (Default port: {port})")
        print(f"     • {BOLD}TTY Redirect: ON{RESET} (Optional, catches printf output)")
        print("-" * 75)
        print("Waiting for Klog Server to come online (Press Ctrl+C to cancel)...")
        while not probe_klog_server(ip, port):
            time.sleep(2)

    print(f"\n{GREEN}✔ Klog Server online! Connecting to {ip}:{port}...{RESET}\n")

    f_out = open(log_file, "a", encoding="utf-8") if log_file else None

    try:
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, port))
                sock.settimeout(None)
                print(f"{GREEN}[CONNECTED] Live stream active. Launch GTA V or trigger mods now.{RESET}\n")

                buffer = ""
                while True:
                    data = sock.recv(4096)
                    if not data:
                        print(f"\n{YELLOW}[DISCONNECTED] Server closed connection. Reconnecting...{RESET}")
                        break
                    
                    buffer += data.decode("utf-8", errors="replace")
                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        formatted = format_line(line)
                        if formatted:
                            print(formatted)
                            if f_out:
                                f_out.write(f"[{datetime.now().isoformat()}] {line.strip()}\n")
                                f_out.flush()

            except (socket.error, ConnectionResetError) as e:
                print(f"{YELLOW}[CONNECTION LOST] {e}. Reconnecting in 3 seconds...{RESET}")
                time.sleep(3)

    except KeyboardInterrupt:
        print(f"\n{CYAN}Monitor session terminated by user.{RESET}")
    finally:
        if f_out:
            f_out.close()

if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    
    parser = argparse.ArgumentParser(description="Live PS4 GoldHEN KLog & Mod Telemetry Monitor")
    parser.add_argument("--ip", default=PS4_IP, help=f"PS4 IP address (default: {PS4_IP})")
    parser.add_argument("--port", type=int, default=KLOG_PORT, help=f"Klog port (default: {KLOG_PORT})")
    parser.add_argument("--output", "-o", default=None, help="Save raw logs to file")
    
    args = parser.parse_args()
    stream_klog(args.ip, args.port, args.output)
