import window_info
import cv2 as cv
import numpy as np
import time
from mss import mss
from pynput import keyboard
from pynput.keyboard import Key, Controller
import logging
import log_message

steering_template = cv.imread('./assets/steering.png', cv.IMREAD_UNCHANGED)
cross_template = cv.imread('./assets/cross_template.png', cv.IMREAD_GRAYSCALE)
cross_template_mask = cv.imread('./assets/cross_template_mask.png', cv.IMREAD_GRAYSCALE)
finish_template = cv.imread('./assets/finish_template.png', cv.IMREAD_GRAYSCALE)
finish_template_mask = cv.imread('./assets/finish_template_mask.png', cv.IMREAD_GRAYSCALE)
worldscreen_template = cv.imread('./assets/worldscreen_template.png', cv.IMREAD_GRAYSCALE)

def draw_preview(title, image):
    global window_rect
    cv.imshow(title, image)
    cv.moveWindow(title, window_rect['left'] + window_rect['width'] - 6, window_rect['top'] - 31)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        exit()

if not window_info.is_window_active():
    print('Chiaki | Stream window not found')


loop_time = time.time()
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

keyboard_controller = Controller()

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
    global keyboard_controller
    keyboard_controller.press('g')
    time.sleep(0.05)
    keyboard_controller.release('g')
    time.sleep(1.0)

# check if there is the cross icon on screen inside the given rectangle
def handle_cross_input(_rect):
    global keyboard_controller
    cross_found = False
    while not cross_found:
        screen_colored = np.array(sct.grab(_rect))
        #draw_preview("Steering", screen_colored)
        screen_grab = cv.cvtColor(screen_colored, cv.COLOR_BGR2GRAY)
        result = cv.matchTemplate(screen_grab, cross_template, cv.TM_CCOEFF_NORMED, cross_template_mask)
        locations = np.where(result >= 0.9)
        locations = list(zip(*locations[::-1]))
        if locations:
            time.sleep(0.2)
            press_cross()
            cross_found = True

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
    handle_cross_input(cross_center_rect)
    time.sleep(1.0)
    logging.info("Starting race")
    press_cross()
    time.sleep(5.0)
    ######################
    # racing        ######
    ######################
    is_racing = True
    is_steering_right = False
    is_steering_left = False
    keyboard_controller.press('5') # throttle
    keyboard_controller.press('6') # nitro / electro boost power

    while is_racing:
        steering_grab = np.array(sct.grab(steering_rect))
        finish_grab =  np.array(sct.grab(finish_rect))
        #draw_preview("Steering", finish_grab)
        height = 15
        width = 15
        errorL2 = cv.norm(steering_grab, steering_template, cv.NORM_L2 )
        similarity = 1 - errorL2 / ( height * width )
        #print('Similarity = ',similarity)
        ## Check if the countersteering icon is white then we need to steer right to keep hugging the wall on the straight
        if not is_steering_right and similarity >= 0.05:
            keyboard_controller.press('d')
            is_steering_right = True
        elif is_steering_right and similarity < 0.05: # release the button if we no longer the to be steering towards the wall
            keyboard_controller.release('d')
            is_steering_right = False

        finish_grab = cv.cvtColor(finish_grab, cv.COLOR_BGR2GRAY)
        result = cv.matchTemplate(finish_grab, finish_template, cv.TM_CCOEFF_NORMED, finish_template_mask)
        locations = np.where(result >= 0.9)
        locations = list(zip(*locations[::-1]))
        if locations:
            is_racing = False
            logging.info("Race finished")        
    if is_steering_right:
        keyboard_controller.release('d')
        is_steering_right = False
    keyboard_controller.release('5')
    keyboard_controller.release('6')

    handle_cross_input(cross_center_rect)
    handle_cross_input(cross_center_rect)
    handle_cross_input(cross_center_rect)
    handle_cross_input(cross_right_rect)
    handle_cross_input(cross_right_rect)
    handle_cross_input(cross_center_rect)
    handle_cross_input(cross_center_rect)
    handle_cross_input(cross_center_rect)
    #TODO add check for roulette ticket!!
    press_cross()
    press_cross()
    time.sleep(1.0)
    press_right()
    press_cross()
    handle_cross_input(cross_center_rect)
    for i in range(3):
        press_right()
    press_cross()
    press_cross()