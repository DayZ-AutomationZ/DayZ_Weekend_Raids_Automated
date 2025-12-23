# Automatic Weekend Raids Mode (cfgGameplay switcher)
[![Automationz.png](https://i.postimg.cc/G29qvGJ3/Automationz.png)](https://postimg.cc/DJkrTWMR)

### TL;DR

1. Copy `raid_mode.py` + both `cfggameplay_raid_*.json` to your Pi.
2. Make the two JSONs full copies of your real `cfggameplay.json` (only toggle the 2 booleans).
3. Add the contents of the real `cfggameplay.json` into both `cfggameplay_raid_*.json`  (remember! only toggle the damage booleans). true / false
4. So `cfggameplay_raid_on.json` and `cfggameplay_raid_off.json`
5. here you set in ON `"disableBaseDamage": false,` and `"disableContainerDamage": false,` or in OFF set `"disableBaseDamage": true,`and `"disableContainerDamage": true,`
7. Put your FTP details into `raid_mode.py`.
8. Test once: `python3 raid_mode.py on` / `off`.
9. Add the cron block to `crontab -e`.
10. Optional BBP Settings  `USE_BBP = False` false is default, set True if you run BaseBuildingPlus. Set it true inside `raid_mode.py` below FTP Credentials
11. If using BBP add `BBP_raid_on.json` and `BBP_raid_off.json` to `/home/PIusername/dayz_raid/` the files are included. Make two JSONs full copies of your real `BBP_Settings.json` (only toggle the 2 booleans).
 Add the contents of the real `BBP_Settings.json` into both `BBP_raid_*.json`  (remember! only toggle the damage booleans). in this case 1 or 0
 so in `BBP_raid_on.json` you set the boolean for `"BBP_DisableDestroy": 0,` so to 0. And in `BBP_raid_off.json` to 1.
 `"BBP_DisableDestroy": 1,` is Raid OFF `"BBP_DisableDestroy": 0,` Raid on.
 Same like `cfggameplay_raid_on.json` and `cfggameplay_raid_off.json`


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

On the Pi, edit cron:

```bash
crontab -e
```

Add this block:

```cron
# --- RAID OFF / ON scheduler) ---
* * * * * /usr/bin/python3 /home/Piusername/dayz_raid/raid_scheduler.py >> /home/PIusername/dayz_raid/raid_scheduler.log 2>&1
```

This does:

- **Fri/Sat/Sun at 18:00**: pushes **RAID-ON** using `raid_scheduler.py` set the time here!
- **Fri/Sat/Sun at 23:59**: pushes **RAID-OFF** again so 00:06 restart comes back up with safe settings.

- `raid_scheduler.py` (set times here) you cannot use 01:05 for example
- it simply is 1, 5 then best times to set are 17, 59 for example: when a server restarts 18:00
- upload files before restart at least a few minutes!, my server restarts 18:06, so 17:59 is a safe choice.
- dont forget to do `chmod +x /home/PIusername/dayz_raid/raid_scheduler.py` and `chmod +x /home/PIusername/dayz_raid/raid_mode.py`
- Set the times on line 17 in `raid_scheduler.py` Line 17: `if dow in (4, 5, 6) and time(17, 59) <= t < time(23, 59):` SO `time(17, 59)` is for Raid ON `time(23, 59)` is for Raid OFF

> You can tweak these times later without touching the Python script – just edit `raid_scheduler.py`

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
