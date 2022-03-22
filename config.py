# if the car doesn't steer try lowering this value
STEERING_SIMILARITY_THRESHOLD = -0.5
# Setting this to True to see the similarity value in the console to 
# help fine tune the steering threshold value. This value should not be 
# lower then the value that is reported when the countersteering icon is red. 
# Otherwise you'll be steering right the whole time and we do not want to do that in corners.
# This will also give you a small window next to the chiaki stream this should display the 
# countersteering icon.
SHOW_SIMILARITY_DEBUG = False
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