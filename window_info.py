from ahk import AHK
from ahk.window import Window

ahk = AHK()
client = None

def is_window_active():
    global client
    return client.id != ''

client = ahk.win_get(title='Chiaki | Stream')

def x():
    return client.rect[0]

def y():
    return client.rect[1]

def width():
    return client.rect[2]
    
def height():
    return client.rect[3]

def focus():
    client.activate()
