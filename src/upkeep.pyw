import subprocess
import time
import threading
import datetime
import os
import sys
import winreg
import re
from pystray import Icon, Menu, MenuItem
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

# --- CONFIGURATION ---
ICON_FILE = 'upkeep_icon.svg'
APP_NAME = "Upkeep"
REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"

# Global state
outdated_apps = [] 
last_check_time = "Never"
check_interval = 3600
stop_event = threading.Event()

def get_icon_image(has_updates):
    try:
        drawing = svg2rlg(ICON_FILE)
        renderPM.drawToFile(drawing, "temp_icon.png", fmt="PNG")
        img = Image.open("temp_icon.png").resize((64, 64))
        if not has_updates:
            img = img.convert("L").convert("RGBA")
        return img
    except Exception:
        from PIL import ImageDraw
        img = Image.new('RGB', (64, 64), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.ellipse((10, 10, 54, 54), fill='blue' if has_updates else 'gray')
        return img

def is_startup_enabled():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
        winreg.QueryValueEx(key, APP_NAME)
        winreg.CloseKey(key)
        return True
    except:
        return False

def toggle_startup(icon, item):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)
    if is_startup_enabled():
        winreg.DeleteValue(key, APP_NAME)
    else:
        script_path = os.path.abspath(sys.argv[0])
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{sys.executable}" "{script_path}"')
    winreg.CloseKey(key)
    icon.menu = create_menu()

def get_outdated_list():
    global outdated_apps, last_check_time
    try:
        result = subprocess.run(['winget', 'upgrade'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        new_list = []
        for line in lines:
            if not line.strip() or '---' in line or 'Name' in line:
                continue
            parts = re.split(r'\s{2,}', line.strip())
            if len(parts) >= 4:
                # We save (Display Name, ID)
                new_list.append((f"{parts[0]} [{parts[2]} -> {parts[3]}]", parts[1]))
        outdated_apps = new_list
        last_check_time = datetime.datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")
        return len(outdated_apps) > 0
    except:
        return False

def check_now(icon):
    has_updates = get_outdated_list()
    icon.icon = get_icon_image(has_updates)
    icon.menu = create_menu()

def update_single(icon, item):
    app_id = next((id for text, id in outdated_apps if text == item.text), None)
    if app_id:
        # Added --force to help with 'in-use' or 'stuck' updates
        command = f'start cmd /c "(echo Upkeep is updating: {app_id}... & winget upgrade --id {app_id} --exact --force --accept-package-agreements --accept-source-agreements) & echo. & echo PROCESS FINISHED. & pause"'
        subprocess.run(command, shell=True)
        threading.Timer(5.0, lambda: check_now(icon)).start()

def update_all(icon):
    # Added --force here as well
    command = 'start cmd /c "(echo Upkeep is updating all software... & winget upgrade --all --force --accept-package-agreements --accept-source-agreements) & echo. & echo ALL UPDATES FINISHED. & pause"'
    subprocess.run(command, shell=True)
    threading.Timer(5.0, lambda: check_now(icon)).start()
    
def set_frequency(icon, item):
    global check_interval
    intervals = {"30 Minutes": 1800, "1 Hour": 3600, "3 Hours": 10800, "6 Hours": 21600, "Once a Day": 86400}
    check_interval = intervals.get(item.text, 3600)
    icon.menu = create_menu()

def create_menu():
    def is_freq_checked(item):
        intervals = {"30 Minutes": 1800, "1 Hour": 3600, "3 Hours": 10800, "6 Hours": 21600, "Once a Day": 86400}
        return check_interval == intervals.get(item.text)

    if outdated_apps:
        outdated_submenu = Menu(*[MenuItem(text, update_single) for text, id in outdated_apps])
    else:
        outdated_submenu = Menu(MenuItem("None", None, enabled=False))
    
    frequency_submenu = Menu(
        MenuItem("30 Minutes", set_frequency, checked=is_freq_checked),
        MenuItem("1 Hour", set_frequency, checked=is_freq_checked),
        MenuItem("3 Hours", set_frequency, checked=is_freq_checked),
        MenuItem("6 Hours", set_frequency, checked=is_freq_checked),
        MenuItem("Once a Day", set_frequency, checked=is_freq_checked)
    )

    return Menu(
        MenuItem(f"{len(outdated_apps)} outdated package(s)", None, enabled=False),
        MenuItem(f"Last checked: {last_check_time}", None, enabled=False),
        Menu.SEPARATOR,
        MenuItem("Start with Windows", toggle_startup, checked=lambda item: is_startup_enabled()),
        Menu.SEPARATOR,
        MenuItem(f"Install updates ({len(outdated_apps)})...", update_all, enabled=len(outdated_apps) > 0),
        MenuItem("Outdated Packages", outdated_submenu),
        MenuItem("Check Frequency", frequency_submenu),
        Menu.SEPARATOR,
        MenuItem("Check for outdated packages now", check_now),
        MenuItem("Exit", lambda icon: icon.stop())
    )

def background_loop(icon):
    check_now(icon)
    while not stop_event.is_set():
        for _ in range(check_interval):
            if stop_event.is_set(): break
            time.sleep(1)
        if not stop_event.is_set():
            check_now(icon)

if __name__ == "__main__":
    icon = Icon(APP_NAME, get_icon_image(False), "Upkeep")
    icon.menu = create_menu()
    thread = threading.Thread(target=background_loop, args=(icon,), daemon=True)
    thread.start()
    icon.run()
    stop_event.set()