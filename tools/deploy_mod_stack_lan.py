#!/usr/bin/env python3
"""
Deploy GTA V v1.56 Mod Stack to PS4 over LAN FTP
Target: PS4 Fat (CUH-1001A @ HEN 11.02 / GoldHEN v2.4b)
"""

import os
import sys
import argparse
import ftplib
from pathlib import Path

DEFAULT_PS4_IP = os.environ.get("PS4_IP", "192.168.1.100")
DEFAULT_FTP_PORT = 2121  # GoldHEN default FTP port is 2121 (or 21)

BASE_DIR = Path(__file__).resolve().parent.parent

def connect_ftp(ip, port):
    print(f"[*] Connecting to PS4 FTP at {ip}:{port}...")
    try:
        ftp = ftplib.FTP()
        ftp.connect(ip, port, timeout=10)
        ftp.login("", "")
        print("[+] Connected successfully to PS4 FTP.")
        return ftp
    except Exception as e:
        print(f"[-] Failed to connect to {ip}:{port}: {e}")
        # Try fallback port 21
        if port == 2121:
            print("[*] Retrying with standard port 21...")
            try:
                ftp = ftplib.FTP()
                ftp.connect(ip, 21, timeout=10)
                ftp.login("", "")
                print("[+] Connected successfully on port 21.")
                return ftp
            except Exception as e2:
                print(f"[-] Fallback failed: {e2}")
        return None

def ensure_remote_dir(ftp, remote_path):
    parts = remote_path.strip("/").split("/")
    current = ""
    for part in parts:
        current += "/" + part
        try:
            ftp.cwd(current)
        except Exception:
            try:
                ftp.mkd(current)
                print(f"  [+] Created remote directory: {current}")
            except Exception as e:
                pass

def upload_file(ftp, local_path, remote_dir, remote_name=None):
    local_path = Path(local_path)
    if not local_path.exists():
        print(f"  [-] Local file not found: {local_path}")
        return False
    
    filename = remote_name if remote_name else local_path.name
    ensure_remote_dir(ftp, remote_dir)
    ftp.cwd(remote_dir)
    
    file_size = local_path.stat().st_size
    print(f"  [>] Uploading {filename} ({file_size:,} bytes) to {remote_dir}/...")
    with open(local_path, "rb") as f:
        ftp.storbinary(f"STOR {filename}", f)
    print(f"  [+] Upload complete: {remote_dir}/{filename}")
    return True

def deploy_patches(ftp):
    print("\n--- [Phase 1] Deploying XML Game Patches (60 FPS, Skip Intro, Snow) ---")
    xml_path = BASE_DIR / "patches" / "GrandTheftAutoV-Orbis.xml"
    upload_file(ftp, xml_path, "/data/GoldHEN/patches/xml")

def deploy_cheats(ftp):
    print("\n--- [Phase 2] Deploying GoldHEN Cheat JSON ---")
    json_path = BASE_DIR / "cheats" / "CUSA00411_01.56.json"
    upload_file(ftp, json_path, "/data/GoldHEN/cheats/json")

def deploy_afr(ftp):
    print("\n--- [Phase 3] Deploying GoldHEN AFR update.rpf ---")
    rpf_path = BASE_DIR / "afr" / "CUSA00411" / "update" / "update.rpf"
    if rpf_path.exists():
        upload_file(ftp, rpf_path, "/data/GoldHEN/AFR/CUSA00411/update")
    else:
        print(f"  [i] Notice: Staged update.rpf not found at {rpf_path}. Skipping AFR upload.")

def deploy_plugins(ftp):
    print("\n--- [Phase 4] Deploying PRX Mod Menus ---")
    prx_path = BASE_DIR / "plugins" / "lotus-base" / "gtav_menu_156.prx"
    if prx_path.exists():
        upload_file(ftp, prx_path, "/data/GoldHEN/plugins")
    else:
        print(f"  [i] Notice: Compiled PRX not found at {prx_path}. Skipping plugin upload.")

def main():
    parser = argparse.ArgumentParser(description="Deploy GTA V 1.56 Mod Stack to PS4")
    parser.add_argument("--ip", default=DEFAULT_PS4_IP, help=f"PS4 IP address (default: {DEFAULT_PS4_IP})")
    parser.add_argument("--port", type=int, default=DEFAULT_FTP_PORT, help=f"FTP port (default: {DEFAULT_FTP_PORT})")
    parser.add_argument("--all", action="store_true", help="Deploy all components (Patches, Cheats, AFR, Plugins)")
    parser.add_argument("--patches", action="store_true", help="Deploy XML Game Patches")
    parser.add_argument("--cheats", action="store_true", help="Deploy GoldHEN Cheat JSON")
    parser.add_argument("--afr", action="store_true", help="Deploy AFR update.rpf")
    parser.add_argument("--plugins", action="store_true", help="Deploy PRX Plugins")

    args = parser.parse_args()

    ftp = connect_ftp(args.ip, args.port)
    if not ftp:
        sys.exit(1)

    try:
        if args.all or (not args.patches and not args.cheats and not args.afr and not args.plugins):
            deploy_patches(ftp)
            deploy_cheats(ftp)
            deploy_afr(ftp)
            deploy_plugins(ftp)
        else:
            if args.patches:
                deploy_patches(ftp)
            if args.cheats:
                deploy_cheats(ftp)
            if args.afr:
                deploy_afr(ftp)
            if args.plugins:
                deploy_plugins(ftp)

        print("\n========================================================")
        print("[+] GTA V Mod Stack Deployment Completed Successfully!")
        print("========================================================")
    finally:
        try:
            ftp.quit()
        except Exception:
            pass

if __name__ == "__main__":
    main()
