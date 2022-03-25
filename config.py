from configparser import ConfigParser
import json

def load_config_file():
    config_file = ConfigParser()
    config_file.read('config.ini')
    
    global STEERING_SIMILARITY_THRESHOLD, USE_RACE_START_MACRO, DPAD_LEFT, DPAD_RIGHT
    global DPAD_UP, DPAD_DOWN, LEFT_STICK_LEFT, LEFT_STICK_RIGHT, LEFT_STICK_UP, LEFT_STICK_DOWN
    global RIGHT_STICK_LEFT, RIGHT_STICK_RIGHT, RIGHT_STICK_UP, RIGHT_STICK_DOWN, L1, L2, L3
    global R1, R2, R3, CROSS, SQUARE, CIRCLE, TRIANGLE, SHARE, OPTIONS, PS, TOUCHPAD
    global SHOW_SIMILARITY_DEBUG, SHOW_DETECTION_RECT_DEBUG, SKIP_MENU_SELECTION
    global STEERING_RECT, CROSS_CENTER_RECT, CROSS_RIGHT_RECT, FINISH_RECT, GT_LOGO_RECT, RACE_START_RECT

    STEERING_SIMILARITY_THRESHOLD = config_file.getfloat('CONFIG', 'STEERING_SIMILARITY_THRESHOLD')
    USE_RACE_START_MACRO = config_file.getboolean('CONFIG', 'USE_RACE_START_MACRO')
    DPAD_LEFT = int(config_file.get('CONTROLS', 'DPAD_LEFT'), 0)
    DPAD_RIGHT = int(config_file.get('CONTROLS', 'DPAD_RIGHT'), 0)
    DPAD_UP = int(config_file.get('CONTROLS', 'DPAD_UP'), 0)
    DPAD_DOWN = int(config_file.get('CONTROLS', 'DPAD_DOWN'), 0)
    LEFT_STICK_LEFT = int(config_file.get('CONTROLS', 'LEFT_STICK_LEFT'), 0)
    LEFT_STICK_RIGHT = int(config_file.get('CONTROLS', 'LEFT_STICK_RIGHT'), 0)
    LEFT_STICK_UP = int(config_file.get('CONTROLS', 'LEFT_STICK_UP'), 0)
    LEFT_STICK_DOWN = int(config_file.get('CONTROLS', 'LEFT_STICK_DOWN'), 0)
    RIGHT_STICK_LEFT = int(config_file.get('CONTROLS', 'RIGHT_STICK_LEFT'), 0)
    RIGHT_STICK_RIGHT = int(config_file.get('CONTROLS', 'RIGHT_STICK_RIGHT'), 0)
    RIGHT_STICK_UP = int(config_file.get('CONTROLS', 'RIGHT_STICK_UP'), 0)
    RIGHT_STICK_DOWN = int(config_file.get('CONTROLS', 'RIGHT_STICK_DOWN'), 0)
    L1 = int(config_file.get('CONTROLS', 'L1'), 0)
    L2 = int(config_file.get('CONTROLS', 'L2'), 0)
    L3 = int(config_file.get('CONTROLS', 'L3'), 0)
    R1 = int(config_file.get('CONTROLS', 'R1'), 0)
    R2 = int(config_file.get('CONTROLS', 'R2'), 0)
    R3 = int(config_file.get('CONTROLS', 'R3'), 0)
    CROSS = int(config_file.get('CONTROLS', 'CROSS'), 0)
    SQUARE = int(config_file.get('CONTROLS', 'SQUARE'), 0)
    CIRCLE = int(config_file.get('CONTROLS', 'CIRCLE'), 0)
    TRIANGLE = int(config_file.get('CONTROLS', 'TRIANGLE'), 0)
    SHARE = int(config_file.get('CONTROLS', 'SHARE'), 0)
    OPTIONS = int(config_file.get('CONTROLS', 'OPTIONS'), 0)
    PS = int(config_file.get('CONTROLS', 'PS'), 0)
    TOUCHPAD = int(config_file.get('CONTROLS', 'TOUCHPAD'), 0)
    SHOW_SIMILARITY_DEBUG = config_file.getboolean('DEBUG', 'SHOW_SIMILARITY_DEBUG')
    SHOW_DETECTION_RECT_DEBUG = config_file.getboolean('DEBUG', 'SHOW_DETECTION_RECT_DEBUG')
    SKIP_MENU_SELECTION = config_file.getboolean('DEBUG', 'SKIP_MENU_SELECTION')

    STEERING_RECT = json.loads(config_file.get('CONFIG', 'STEERING_RECT'))
    CROSS_CENTER_RECT = json.loads(config_file.get('CONFIG', 'CROSS_CENTER_RECT'))
    CROSS_RIGHT_RECT = json.loads(config_file.get('CONFIG', 'CROSS_RIGHT_RECT'))
    FINISH_RECT = json.loads(config_file.get('CONFIG', 'FINISH_RECT'))
    GT_LOGO_RECT = json.loads(config_file.get('CONFIG', 'GT_LOGO_RECT'))  
    RACE_START_RECT = json.loads(config_file.get('CONFIG', 'RACE_START_RECT'))    

def get_key_for_string(key):
    return globals()[key]

STEERING_RECT = { 'left' : 863, 'top' : 649, 'width' : 15, 'height' : 15 }
CROSS_CENTER_RECT = { 'left' : 580, 'top' : 630, 'width' : 80, 'height' : 80 }
CROSS_RIGHT_RECT = { 'left' : 1150, 'top' : 620, 'width' : 60, 'height' : 60, }
FINISH_RECT = { 'left' : 450, 'top' : 310, 'width' : 100, 'height' : 100 }
GT_LOGO_RECT = {'left' : 0, 'top' : 0, 'width' : 70, 'height' : 70 }
RACE_START_RECT = { 'left' : 600, 'top' : 320, 'width' : 80, 'height' : 80 }
CROSS_ICON_CHECK_THRESHOLD = 0.85
FINISH_CHECK_THRESHOLD = 0.85
GT_LOGO_CHECK_THRESHOLD = 0.85
RACE_START_CHECK_THRESHOLD = 0.85

# if the car doesn't steer try lowering this value
STEERING_SIMILARITY_THRESHOLD = -5.0
# Setting this to True to see the similarity value in the console to 
# help fine tune the steering threshold value. This value should not be 
# lower then the value that is reported when the countersteering icon is red. 
# Otherwise you'll be steering right the whole time and we do not want to do that in corners.
# This will also give you a small window next to the chiaki stream this should display the 
# countersteering icon.
SHOW_SIMILARITY_DEBUG = False
SHOW_DETECTION_RECT_DEBUG = False
# Skip menu selection is useful if you want the tweak the race start macro. This way you can just restart the bot and click restart race.
SKIP_MENU_SELECTION = False
USE_RACE_START_MACRO = True
# Input keys. These need to match with what is set in Chiaki.
# https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
DPAD_LEFT = 0x25
DPAD_RIGHT = 0x27
DPAD_UP = 0x26
DPAD_DOWN = 0x28
LEFT_STICK_LEFT = 0x41
LEFT_STICK_RIGHT = 0x44
LEFT_STICK_UP = 0x57
LEFT_STICK_DOWN = 0x53
RIGHT_STICK_LEFT = 0x4A
RIGHT_STICK_RIGHT = 0x4C
RIGHT_STICK_UP = 0x49
RIGHT_STICK_DOWN = 0x4B
L1 = 0x31
L2 = 0x32
L3 = 0x33
R1 = 0x34
R2 = 0x35
R3 = 0x36
CROSS = 0x47
SQUARE = 0x46
CIRCLE = 0x54
TRIANGLE = 0x52
SHARE = 0x50
OPTIONS = 0x4F
PS = 0x1B
TOUCHPAD = 0x09