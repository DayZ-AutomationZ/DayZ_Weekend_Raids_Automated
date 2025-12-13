#!/usr/bin/python3
from datetime import datetime, time
from pathlib import Path
import subprocess
import json

BASE = Path("/home/PIusername/dayz_raid")
STATE_FILE = BASE / "raid_state.json"
RAID_MODE = BASE / "raid_mode.py"

def desired_state(now: datetime) -> str:
    # Python: Mon=0 ... Sun=6
    dow = now.weekday()
    t = now.time()

    # Weekend raid window: Fri/Sat/Sun from 17:59 up to (but not including) 23:59
    if dow in (4, 5, 6) and time(17, 59) <= t < time(23, 59):
        return "on"
    return "off"

def load_last() -> str:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text()).get("state", "")
        except Exception:
            return ""
    return ""

def save_last(state: str, now: datetime):
    STATE_FILE.write_text(json.dumps({"state": state, "ts": now.isoformat()}, indent=2))

def run(mode: str):
    # call your existing script
    subprocess.run(["/usr/bin/python3", str(RAID_MODE), mode], check=False)

def main():
    now = datetime.now()
    want = desired_state(now)
    last = load_last()

    if want != last:
        print(f"[{now}] state change: {last} -> {want}")
        run(want)
        save_last(want, now)
    else:
        print(f"[{now}] no change: {want}")

if __name__ == "__main__":
    main()

