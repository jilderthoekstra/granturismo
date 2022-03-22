import window_info
import cv2 as cv
import numpy as np
import time
import config
import logging
import log_message
from threading import Thread

def draw_preview(title, image):
    cv.imshow(title, image)
    cv.moveWindow(title, window.x + window.width - 6, window.offset_y)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        exit()

def draw_rectangles():
    while True:
        rect = { 'left' : 0, 'top' : 0, 'width': window.content_width, 'height': window.content_height }
        rect_color = (255, 255, 255) # BGR
        image = window.grab(rect)
        rectangles = {
            "Steering" : steering_rect,
            "Cross Center" : cross_center_rect,
            "Cross Right" : cross_right_rect,
            "Finish (F)" : finish_rect,
            "GT Logo" : gt_logo_rect
        }

        font = cv.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        text_color = (255, 255, 255)
        text_thickness = 1
        for key, value in rectangles.items():
            image = cv.rectangle(image, (value['left'], value['top']), (value['left'] + value['width'], value['top'] + value['height']), rect_color, 2)
            text_position = [value['left'], value['top'] - 10]
            if value['top'] < 10:
                text_position[1] = value['top'] + value['height'] + 15        
            image = cv.putText(image, key, text_position, font, font_scale, text_color, text_thickness, cv.LINE_AA)    
        cv.imshow("Detection Rectangles | Press q to close this window. After that terminate program ctrl+c", image)

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()

# check if there is the cross icon on screen inside the given rectangle
def handle_cross_input(rects, timeout=99.0):
    start_time = time.time()
    while timeout > time.time() - start_time:
        for r in rects:
            screen_colored = np.array(window.grab(r))
            screen_grab = cv.cvtColor(screen_colored, cv.COLOR_BGR2GRAY)
            result = cv.matchTemplate(screen_grab, cross_template, cv.TM_CCOEFF_NORMED, cross_template_mask)
            locations = np.where(result >= 0.9) # if there are problems detecting the icon you can try lowering this value
            locations = list(zip(*locations[::-1]))
            if locations:
                time.sleep(0.2)
                window.key_click(config.CROSS, 0.2)
                return True
    return False

# check for the top left logo to see if we are back on the homescreen (this may or may not work if you still have cafe missions active)
def wait_for_gt_logo():
    gt_logo_found = False
    while not gt_logo_found:
        screen_colored = np.array(window.grab(gt_logo_rect))
        #draw_preview("Waiting For WorldScreen", screen_colored)
        screen_grab = cv.cvtColor(screen_colored, cv.COLOR_BGR2GRAY)
        result = cv.matchTemplate(screen_grab, worldscreen_template, cv.TM_CCOEFF_NORMED)
        locations = np.where(result >= 0.9) # if there are problems detecting the logo you can try lowering this value
        locations = list(zip(*locations[::-1]))
        if locations:
            time.sleep(0.2)
            gt_logo_found = True
        time.sleep(0.5)

def handle_steering_with_similarity_check(is_steering_right):
    steering_grab = np.array(window.grab(steering_rect))
    errorL2 = cv.norm(steering_grab, steering_template, cv.NORM_L2 )
    similarity = 1 - errorL2 / ( steering_rect['height'] * steering_rect['width'] )
    if config.SHOW_SIMILARITY_DEBUG:
        draw_preview("Steering Icon", steering_grab)
        logging.info('Similarity: {}'.format(similarity))

    # Check if the countersteering icon is white then we need to steer right to keep hugging the wall on the straight
    if not is_steering_right and similarity >= config.STEERING_SIMILARITY_THRESHOLD:
        window.key_down(config.LEFT_STICK_RIGHT)
        return True
    elif is_steering_right and similarity < config.STEERING_SIMILARITY_THRESHOLD: # release the button if we no longer the to be steering towards the wall
        window.key_up(config.LEFT_STICK_RIGHT)
        return False
    return is_steering_right

def has_reached_finished():
    finish_grab =  np.array(window.grab(finish_rect))
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

window = window_info.WindowInfo()

logging.info('Looking for chiaki window')
if not window.is_active():
    logging.info('Chiaki | Stream window not found')
    exit()
else:
    logging.info('Chiaki window found.')

logging.info('Window content size width: {} height: {}'.format(window.content_width, window.content_height))

steering_rect = {
    'left' : 863,
    'top' : 649,
    'width' : 15,
    'height' : 15,
}

cross_center_rect = {
    'left' : 600,
    'top' : 630,
    'width' : 40,
    'height' : 80,
}

cross_right_rect = {
    'left' : 1160,
    'top' : 630,
    'width' : 40,
    'height' : 40,
}

finish_rect = {
    'left' : 460,
    'top' : 320,
    'width' : 80,
    'height' : 80,
}

gt_logo_rect = {
    'left' : 0,
    'top' : 0,
    'width' : 60,
    'height' : 60,
}

cross_icon_locations = [ cross_center_rect, cross_right_rect ]

if config.SHOW_DETECTION_RECT_DEBUG:
    t = Thread(target = draw_rectangles)
    t.start() 

logging.info("Starting bot")
time.sleep(0.5)
while True:
    logging.info("Waiting for worldscreen")
    wait_for_gt_logo()
    logging.info("Selecting championship")
    window.key_click(config.DPAD_DOWN, 0.5)
    for i in range(6):
        window.key_click(config.DPAD_RIGHT, 0.2)
    window.key_click(config.CROSS, 1.0)
    window.key_click(config.CROSS, 0.5)
    logging.info("Waiting for race start screen")
    handle_cross_input([cross_center_rect])
    wait_for_gt_logo()
    logging.info("Starting race")
    window.key_click(config.CROSS, 0.5)
    time.sleep(5.0)

    ######################
    # racing        ######
    ######################
    is_racing = True
    is_steering_right = False

    window.key_down(config.R2) # throttle
    window.key_down(config.R3) # nitro / electro boost power

    while is_racing:
        is_steering_right = handle_steering_with_similarity_check(is_steering_right)
        is_racing = not has_reached_finished()
        # let's wait a bit to keep cpu usage low.
        time.sleep(0.033)

    # release controls after race has finished
    if is_steering_right:
        window.key_up(config.LEFT_STICK_RIGHT)
        is_steering_right = False
    window.key_up(config.R2)
    window.key_up(config.R3)

    # check for the cross icon after the race (20 second timeout)
    handle_cross_input([cross_center_rect], 20) 
    # check for the cross icon in the menu. We'll keep checking for icons. With a 3.0 second timeout
    # if after 3.0 seconds we don't find an icon then we'll probably be in the replay mode
    # and can move on. This also handles the roulette ticket screen. If for on PS4 loading takes longer
    # between menu's then increase the 3.0 value
    while handle_cross_input(cross_icon_locations, 3.0):
        time.sleep(1.0)

    window.key_click(config.CROSS, 0.5)   # press cross to active hud in replay
    window.key_click(config.CROSS, 0.5)
    wait_for_gt_logo()
    window.key_click(config.DPAD_RIGHT, 0.2)
    window.key_click(config.CROSS, 0.2)
    handle_cross_input([cross_center_rect])
    wait_for_gt_logo()
    for i in range(3): # move cursor to exit button
        window.key_click(config.DPAD_RIGHT, 0.2)
    window.key_click(config.CROSS, 0.5)
    window.key_click(config.CROSS, 0.5)
    time.sleep(5.0)

