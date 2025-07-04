import numpy as np
from mss import mss
import time
import screen_brightness_control as sbc
import pystray
import sys
import threading
from PIL import Image

auto_mode = True
running = True

def set_brightness_from_screen(frame):
    gray = np.mean(frame[:,:,:3]) #calculating the average brightness of the screen as th mean value of R G B channels of all pixels on the screen

    brightness = int(100 - (gray/255)*100)

    brightness = max(15,min(brightness,100))

    sbc.set_brightness(brightness)


def brightness_loop():
    global auto_mode, running

    with mss() as sct:
        monitor = sct.monitors[1]

        while running:
            if auto_mode:
                img = sct.grab(monitor) #grabbing the real time contents of the screen

                frame = np.array(img) #converting the image to a numpy 3D array

                set_brightness_from_screen(frame)

            time.sleep(0.1)

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
    icon_image = Image.open('brightness.png').resize((64,64)).convert('RGBA')
    menu = pystray.Menu(
        pystray.MenuItem("Toggle Auto brightness", toggle_auto),
        pystray.MenuItem("Quit", quit_app)
    )
    icon = pystray.Icon("AutoBrightness", icon_image, "Auto Brightness (ON ✅)", menu)
    icon.run()

    

if __name__ == "__main__":
    threading.Thread(target=brightness_loop, daemon=True).start()

    tray()