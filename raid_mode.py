import ftplib
import sys
from pathlib import Path

# ==============================
# CONFIGURE THESE VALUES FOR YOUR SERVERS FTP.
# ==============================
FTP_HOST = "YOUR_FTP_HOST"
FTP_USER = "YOUR_FTP_USERNAME"
FTP_PASS = "YOUR_FTP_PASSWORD"

# Remote path where cfgGameplay.json lives on your host
# Example for Nitrado: /dayzstandalone/mpmissions/dayzOffline.chernarusplus
REMOTE_DIR = "/dayzstandalone/mpmissions/dayzOffline.chernarusplus"
REMOTE_CFG = "cfggameplay.json"

# Local folder on the Pi where your templates live
LOCAL_DIR = Path("/home/PIusername/dayz_raid")  # adjust username if needed

def upload_cfg(mode: str):
    if mode == "on":
        local_file = LOCAL_DIR / "cfggameplay_raid_on.json"
    elif mode == "off":
        local_file = LOCAL_DIR / "cfggameplay_raid_off.json"
    else:
        raise SystemExit("Mode must be 'on' or 'off'")

    if not local_file.exists():
        raise SystemExit(f"Local config not found: {local_file}")

    print(f"[Raid {mode.upper()}] Connecting to FTP...")
    with ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS) as ftp:
        ftp.cwd(REMOTE_DIR)
        with open(local_file, "rb") as f:
            print(f"[Raid {mode.upper()}] Uploading {local_file.name} -> {REMOTE_CFG}")
            ftp.storbinary(f"STOR {REMOTE_CFG}", f)
    print(f"[Raid {mode.upper()}] Upload complete.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 raid_mode.py on|off")
        raise SystemExit(1)
    upload_cfg(sys.argv[1])
