import ftplib
import sys
from pathlib import Path
from datetime import datetime

print(f"[CRON] raid_mode.py started at {datetime.now()}")

FTP_HOST = "FTP.HOST.COM"
FTP_USER = "username"
FTP_PASS = "password"

# Remote paths
REMOTE_GAMEPLAY_DIR = "/dayzstandalone/mpmissions/dayzOffline.chernarusplus"
REMOTE_GAMEPLAY_CFG = "cfggameplay.json"

REMOTE_BBP_DIR = "/dayzstandalone/config/BaseBuildingPlus"
REMOTE_BBP_CFG = "BBP_Settings.json"

# Local folder on the Pi
LOCAL_DIR = Path("/home/PIusername/dayz_raid")

def upload_file(ftp, local_path: Path, remote_dir: str, remote_name: str):
    if not local_path.exists():
        raise SystemExit(f"Local config not found: {local_path}")
    ftp.cwd(remote_dir)
    with open(local_path, "rb") as f:
        print(f"Uploading {local_path.name} -> {remote_dir}/{remote_name}")
        ftp.storbinary(f"STOR {remote_name}", f)

def upload_cfg(mode: str):
    if mode == "on":
        local_gameplay = LOCAL_DIR / "cfggameplay_raid_on.json"
        local_bbp      = LOCAL_DIR / "BBP_raid_on.json"
    elif mode == "off":
        local_gameplay = LOCAL_DIR / "cfggameplay_raid_off.json"
        local_bbp      = LOCAL_DIR / "BBP_raid_off.json"
    else:
        raise SystemExit("Mode must be 'on' or 'off'")

    print(f"[Raid {mode.upper()}] Connecting to FTP...")
    with ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS) as ftp:
        # Upload cfggameplay
        upload_file(ftp, local_gameplay, REMOTE_GAMEPLAY_DIR, REMOTE_GAMEPLAY_CFG)
        # Upload BBP settings
        upload_file(ftp, local_bbp, REMOTE_BBP_DIR, REMOTE_BBP_CFG)

    print(f"[Raid {mode.upper()}] Upload complete.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python raid_mode.py on|off")
        raise SystemExit(1)
    upload_cfg(sys.argv[1])


