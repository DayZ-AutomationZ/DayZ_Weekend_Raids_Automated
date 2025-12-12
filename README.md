# Automatic Weekend Raids Mode (cfgGameplay switcher)
[![Day-Z-Automation-Z-(1).png](https://i.postimg.cc/cC0H7Jh0/Day-Z-Automation-Z-(1).png)](https://postimg.cc/PpVTTT0R)

### TL;DR

1. Copy `raid_mode.py` + both `cfggameplay_raid_*.json` to your Pi.
2. Make the two JSONs full copies of your real `cfggameplay.json` (only toggle the 2 booleans).
3. Add the contents of the real `cfggameplay.json` into both `cfggameplay_raid_*.json`  (remember! only toggle the damage booleans). true / false
4. Put your FTP details into `raid_mode.py`.
5. Test once: `python3 raid_mode.py on` / `off`.
6. Add the cron block to `crontab -e`.

This package lets your Raspberry Pi automatically toggle DayZ **raid mode** on your Nitrado server by uploading different `cfggameplay.json` files via FTP.
NO NEED FOR MODS! just simple ftp uploads from your PI VPS or any machine running python to your server to change 2 values in `cfggameplay.json`

- **Raid ON:** `disableBaseDamage = false`, `disableContainerDamage = false`  
- **Raid OFF:** `disableBaseDamage = true`,  `disableContainerDamage = true`  
- Fully external: **no extra DayZ mods** required.
- Works great with a raid schedule like **Friday–Sunday, 18:00–00:00**.

---

## 1. Files in this package

Put these on your Raspberry Pi:

```text
/home/PIusername/dayz_raid/
├── raid_mode.py
├── cfggameplay_raid_on.json
└── cfggameplay_raid_off.json
```

If your username is not `PIusername`, just adjust the paths in `raid_mode.py` and in your `crontab` later.

---

## 2. Prepare the templates (VERY IMPORTANT)

1. **Download your current live `cfggameplay.json`** from Nitrado:  
   `dayzstandalone/mpmissions/dayzOffline.chernarusplus/cfggameplay.json`

2. Open it on your PC and **save two copies**:
   - `cfggameplay_raid_on.json`
   - `cfggameplay_raid_off.json`

3. For **both copies**, keep EVERYTHING exactly the same except:  
   In the `GeneralData` block, set:

   - For **raid ON** (`cfggameplay_raid_on.json`):
     ```json
     "disableBaseDamage": false,
     "disableContainerDamage": false
     ```

   - For **raid OFF** (`cfggameplay_raid_off.json`):
     ```json
     "disableBaseDamage": true,
     "disableContainerDamage": true
     ```

4. Upload those 2 prepared files to your Pi into:
   ```text
   /home/PIusername/dayz_raid/
   ```

5. On the Pi, **delete** the placeholder `.json` templates from this package or overwrite them with your real ones.

> ⚠️ If you forget to copy the full file and only use the small example, your server will NOT start. Always use the full original content with only those 2 booleans changed. (true or false)

---

## 3. Edit `raid_mode.py` with your FTP details ⚠️ Don’t share screenshots of this file, it contains your FTP password.

Open `raid_mode.py` on the Pi and set:

```python
FTP_HOST = "YOUR_FTP_HOST"
FTP_USER = "YOUR_FTP_USERNAME"
FTP_PASS = "YOUR_FTP_PASSWORD"

REMOTE_DIR = "/dayzstandalone/mpmissions/dayzOffline.chernarusplus"
REMOTE_CFG = "cfggameplay.json"
LOCAL_DIR = Path("/home/PIusername/dayz_raid")
```

- `FTP_HOST`, `FTP_USER`, `FTP_PASS` → from your Nitrado FTP panel.  
- Leave `REMOTE_DIR` and `REMOTE_CFG` as is unless your host uses a different path.

Test it manually from the Pi:

```bash
cd /home/PIusername/dayz_raid
python3 raid_mode.py off   # uploads the RAID-OFF cfgGameplay.json
```

Check on FTP that `cfggameplay.json` on the server changed and try to start the server. If it works, the script is good.

---

## 4. Hook into your raid schedule with cron

We’ll assume:

- Server restarts: **00:06**, **06:09**, **12:09**, **18:08**
- Raid times: **Friday, Saturday, Sunday – 18:00–00:00**
- Pi user: **d3nd4n**

On the Pi, edit cron:

```bash
crontab -e
```

Add this block **below** your existing ClaimBot line:

```cron
# --- RAID OFF BEFORE ALL RESTARTS (EVERY DAY) ---
0 0 * * * python3 /home/PIusername/dayz_raid/raid_mode.py off
5 6 * * * python3 /home/PIusername/dayz_raid/raid_mode.py off
5 12 * * * python3 /home/PIusername/dayz_raid/raid_mode.py off
5 18 * * * python3 /home/PIusername/dayz_raid/raid_mode.py off

# --- RAID OFF AT END OF RAID WINDOW (23:59 FRI/SAT/SUN) ---
59 23 * * 5 python3 /home/PIusername/dayz_raid/raid_mode.py off
59 23 * * 6 python3 /home/PIusername/dayz_raid/raid_mode.py off
59 23 * * 0 python3 /home/PIusername/dayz_raid/raid_mode.py off

# --- RAID ON AT 18:00 (FRI/SAT/SUN) ---
0 18 * * 5 python3 /home/PIusername/dayz_raid/raid_mode.py on
0 18 * * 6 python3 /home/PIusername/dayz_raid/raid_mode.py on
0 18 * * 0 python3 /home/PIusername/dayz_raid/raid_mode.py on
```

This does:

- **Every day**: pushes **RAID-OFF** config shortly before your restarts.  
- **Fri/Sat/Sun at 18:00**: pushes **RAID-ON** config.  
- **Fri/Sat/Sun at 23:59**: pushes **RAID-OFF** again so 00:06 restart comes back up with safe settings.

> You can tweak these times later without touching the Python script – just edit your crontab.

---

## 5. How it works

- DayZ reads **only one** `cfggameplay.json` at startup.
- The Pi uploads the correct version (`raid_on` or `raid_off`) via FTP **before** your server restarts or during raid-window switches.
- After restart, the server comes up in the right mode:
  - **Raiding allowed** during your window.
  - **Safe base-building** outside of it.

No in‑game messages are needed; you can announce raid times via Discord, loading screen, or billboards.

---

## 6. Safety tips

- Always keep a **backup** of your original `cfggameplay.json` somewhere safe.
- If you mess something up and the server won’t start:
  1. Stop the server.
  2. Re-upload your original `cfggameplay.json` via FTP.
  3. Start the server again.
- After everything works, commit your `.py` and `.json` in git or a backup folder so you never lose your setup.

Have fun raiding only when **Your server** says it’s time. 🦌🔨 YOU NEED TO SET UP THE TIME CORRECT WITH YOUR SERVER RESTARTS. 

The server used for this code had the following server restarts. 
Make Sure to set the time on the PI or whatever server you use the same as your game server

game_server_restart	Time: 00:06
Last Run: 09-12-2025 00:06:14 UTC +01:00
Next Run: 10-12-2025 00:06:00 UTC +01:00	Automated server restart in progress...	
game_server_restart	Time: 06:09
Last Run: 08-12-2025 06:10:04 UTC +01:00
Next Run: 09-12-2025 06:09:00 UTC +01:00	Automated server restart in progress...	
game_server_restart	Time: 12:09
Last Run: 08-12-2025 12:09:43 UTC +01:00
Next Run: 09-12-2025 12:09:00 UTC +01:00	Automated server restart in progress...	
game_server_restart	Time: 18:08
Last Run: 08-12-2025 18:08:20 UTC +01:00
Next Run: 09-12-2025 18:08:00 UTC +01:00	Automated server restart in progress...
