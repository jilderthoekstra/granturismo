import window_info
import cv2 as cv
import numpy as np
import time
from mss import mss
from pynput import keyboard
from pynput.keyboard import Key, Controller
import config
import logging
import log_message

def draw_preview(title, image):
    cv.imshow(title, image)
    cv.moveWindow(title, window_rect['left'] + window_rect['width'] - 6, window_rect['top'] - 31)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        exit()

def press_down():
    keyboard_controller.press(Key.down)
    time.sleep(0.05)
    keyboard_controller.release(Key.down)
    time.sleep(0.2)

def press_right():
    keyboard_controller.press(Key.right)
    time.sleep(0.05)
    keyboard_controller.release(Key.right)
    time.sleep(0.2)

def press_cross():
    keyboard_controller.press('g')
    time.sleep(0.05)
    keyboard_controller.release('g')
    time.sleep(1.0)

# check if there is the cross icon on screen inside the given rectangle
def handle_cross_input(rects, timeout=99.0):
    start_time = time.time()
    while timeout > time.time() - start_time:
        for r in rects:
            screen_colored = np.array(sct.grab(r))
            screen_grab = cv.cvtColor(screen_colored, cv.COLOR_BGR2GRAY)
            result = cv.matchTemplate(screen_grab, cross_template, cv.TM_CCOEFF_NORMED, cross_template_mask)
            locations = np.where(result >= 0.9)
            locations = list(zip(*locations[::-1]))
            if locations:
                time.sleep(0.2)
                press_cross()
                return True
    return False

# check for the top left logo to see if we are back on the homescreen (this may or may not work if you still have cafe missions active)
def wait_for_worldscreen():
    world_screen_found = False
    while not world_screen_found:
        screen_colored = np.array(sct.grab(worldscreen_rect))
        #draw_preview("Steering", screen_colored)
        screen_grab = cv.cvtColor(screen_colored, cv.COLOR_BGR2GRAY)
        result = cv.matchTemplate(screen_grab, worldscreen_template, cv.TM_CCOEFF_NORMED)
        locations = np.where(result >= 0.9)
        locations = list(zip(*locations[::-1]))
        if locations:
            time.sleep(0.2)
            world_screen_found = True
        time.sleep(0.5)

def handle_steering_with_similarity_check(is_steering_right):
    steering_grab = np.array(sct.grab(steering_rect))
    errorL2 = cv.norm(steering_grab, steering_template, cv.NORM_L2 )
    similarity = 1 - errorL2 / ( steering_rect['height'] * steering_rect['width'] )
    if config.SHOW_SIMILARITY_DEBUG:
        draw_preview("Steering Icon", steering_grab)
        logging.info('Similarity: {}'.format(similarity))

    # Check if the countersteering icon is white then we need to steer right to keep hugging the wall on the straight
    if not is_steering_right and similarity >= config.STEERING_SIMILARITY_THRESHOLD:
        keyboard_controller.press('d')
        return True
    elif is_steering_right and similarity < config.STEERING_SIMILARITY_THRESHOLD: # release the button if we no longer the to be steering towards the wall
        keyboard_controller.release('d')
        return False
    return is_steering_right

def has_reached_finished():
    finish_grab =  np.array(sct.grab(finish_rect))
    finish_grab = cv.cvtColor(finish_grab, cv.COLOR_BGR2GRAY)
    result = cv.matchTemplate(finish_grab, finish_template, cv.TM_CCOEFF_NORMED, finish_template_mask)
    locations = np.where(result >= 0.9)
    locations = list(zip(*locations[::-1]))
    if locations:
        logging.info("Race finished")        
        return True
    return False


steering_template = cv.imread('./assets/steering.png', cv.IMREAD_UNCHANGED)
cross_template = cv.imread('./assets/cross_template.png', cv.IMREAD_GRAYSCALE)
cross_template_mask = cv.imread('./assets/cross_template_mask.png', cv.IMREAD_GRAYSCALE)
finish_template = cv.imread('./assets/finish_template.png', cv.IMREAD_GRAYSCALE)
finish_template_mask = cv.imread('./assets/finish_template_mask.png', cv.IMREAD_GRAYSCALE)
worldscreen_template = cv.imread('./assets/worldscreen_template.png', cv.IMREAD_GRAYSCALE)

logging.info('Looking for chiaki window')
if not window_info.is_window_active():
    logging.info('Chiaki | Stream window not found')
    exit()
else:
    logging.info('Chiaki window found.')

sct = mss()
window_rect = { 
    'left' : window_info.x() + 10,
    'top' : window_info.y() + 31,
    'width' : window_info.width() - 20,
    'height' : window_info.height() - 39,
}

steering_rect = {
    'left' : window_rect['left'] + 861,
    'top' : window_rect['top'] + 649,
    'width' : 15,
    'height' : 15,
}

cross_center_rect = {
    'left' : window_rect['left'] + 600,
    'top' : window_rect['top'] + 630,
    'width' : 40,
    'height' : 80,
}

cross_right_rect = {
    'left' : window_rect['left'] + 1160,
    'top' : window_rect['top'] + 630,
    'width' : 40,
    'height' : 40,
}

finish_rect = {
    'left' : window_rect['left'] + 460,
    'top' : window_rect['top'] + 320,
    'width' : 80,
    'height' : 80,
}

worldscreen_rect = {
    'left' : window_rect['left'],
    'top' : window_rect['top'],
    'width' : 60,
    'height' : 60,
}

cross_icon_locations = [ cross_center_rect, cross_right_rect ]

keyboard_controller = Controller()

window_info.focus()
logging.info("Starting bot")
time.sleep(0.5)
while True:
    logging.info("Waiting for worldscreen")
    wait_for_worldscreen()
    logging.info("Select championship")
    press_down()
    for i in range(6):
        press_right()
    press_cross()
    press_cross()
    handle_cross_input([cross_center_rect])
    time.sleep(1.0)
    logging.info("Starting race")
    press_cross()
    time.sleep(5.0)

    ######################
    # racing        ######
    ######################
    is_racing = True
    is_steering_right = False

    keyboard_controller.press('5') # throttle
    keyboard_controller.press('6') # nitro / electro boost power

    while is_racing:
        is_steering_right = handle_steering_with_similarity_check(is_steering_right)
        is_racing = not has_reached_finished()
        # let's wait a bit to keep cpu usage low.
        time.sleep(0.033)

    # release controls after race has finished
    if is_steering_right:
        keyboard_controller.release('d')
        is_steering_right = False
    keyboard_controller.release('5')
    keyboard_controller.release('6')

    # check for the cross icon after the race (20 second timeout)
    handle_cross_input([cross_center_rect], 20) 
    # check for the cross icon in the menu. We'll keep checking for icons. With a 3.0 second timeout
    # if after 3.0 seconds we don't find an icon then we'll probably be in the replay mode
    # and can move on. This also handles the roulette ticket screen. If for on PS4 loading takes longer
    # between menu's then increase the 3.0 value
    while handle_cross_input(cross_icon_locations, 3.0):
        time.sleep(1.0)

    press_cross()   # press cross to active hud in replay
    press_cross()
    time.sleep(1.0)
    press_right()
    press_cross()
    handle_cross_input([cross_center_rect])
    for i in range(3): # move cursor to exit button
        press_right()
    press_cross() # exit championship
    press_cross() # confirm exit