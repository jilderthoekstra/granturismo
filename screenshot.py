from pynput import keyboard
from pynput.keyboard import Key, Controller
import window_info
from time import time

keyboard_controller = Controller()

window = window_info.WindowInfo()

window_rect = { 
    'left' : 0,
    'top' : 0,
    'width' : window.content_width,
    'height' : window.content_height,
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
    name = './{0}/{1}.bmp'.format(folder, time())
    window.save(window_rect, name)
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