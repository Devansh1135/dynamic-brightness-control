import numpy as np
from mss import mss
import time
import screen_brightness_control as sbc
import pystray
import sys
import threading
from PIL import Image
import os

def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

auto_mode = True
running = True
day_mode = False

def set_brightness_from_screen(frame):
    gray = np.mean(frame[:,:,:3]) #calculating the average brightness of the screen as th mean value of R G B channels of all pixels on the screen

    brightness = int(100 - (gray/255)*100)

    brightness_night = max(15,min(brightness,100))
    brightness_day = max(60,min(brightness,100))

    if day_mode == True:
        sbc.set_brightness(brightness_day)
    else : 
        sbc.set_brightness(brightness_night)


def brightness_loop():
    global auto_mode, running, day_mode

    with mss() as sct:
        monitor = sct.monitors[1]

        while running:
            if auto_mode:
                
                img = sct.grab(monitor) #grabbing the real time contents of the screen

                frame = np.array(img) #converting the image to a numpy 3D array

                set_brightness_from_screen(frame)

            time.sleep(0.1)

def toggle_day_night(icon,item):
    global day_mode
    day_mode = not day_mode
    status = "🌞 Day mode on" if day_mode else "🌜 Night mode on"
    print(status)
    icon.title = status

def toggle_auto(icon,item):
    global auto_mode
    auto_mode = not auto_mode
    status = "ON ✅" if auto_mode else "OFF ❌"
    print(f"auto mode toggled : {status}")
    icon.title = f"auto brightness {status}"

def quit_app(icon,item):
    global running
    running = False
    icon.stop()
    print("Exiting...")

def tray():
    
    icon_image = Image.open(resource_path('brightness.ico')).resize((64, 64)).convert('RGBA')

    menu = pystray.Menu(
        pystray.MenuItem("Day mode / Night mode" , toggle_day_night),
        pystray.MenuItem("Toggle Auto brightness", toggle_auto),
        pystray.MenuItem("Quit", quit_app)
    )
    icon = pystray.Icon("AutoBrightness", icon_image, "Auto Brightness (ON ✅)", menu)
    icon.run()

    

if __name__ == "__main__":
    threading.Thread(target=brightness_loop, daemon=True).start()

    tray()