from pynput import keyboard
from pynput.keyboard import Key, Controller
import mss
import mss.tools
import window_info
from time import time

keyboard_controller = Controller()

window_rect = { 
    'left' : window_info.x() + 10,
    'top' : window_info.y() + 31,
    'width' : window_info.width() - 20,
    'height' : window_info.height() - 41,
}

def on_press(key):
    pass

def on_release(key):
    global count_positive, count_negative
    if key == Key.esc:
        # Stop listener
        return False
    elif hasattr(key, 'char') and key.char == ']':
        save_screenshot('screenshots')

def save_screenshot(folder):
    global window_rect
    name = './{0}/{1}.png'.format(folder, time())
    with mss.mss() as sct:    
        sct_img = sct.grab(window_rect)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=name)
    print('Saved screenshot '+ name)

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

def main():
    while True:
        pass

if __name__ == "__main__":
    main()