

from time import sleep
from contextlib import contextmanager
from pathlib import Path
from random import randint, choice

from seleniumbase import Driver
import pyautogui


# sleep func to prevent bot detection *********************************************************************

def more_or_less(number: float) -> float:
    sign = choice([1, -1])
    delta = randint(1, 100) / 1000
    return number * (1 + sign * delta)


def slow_down(second: float) -> None:
    """sleep for around seond"""
    sleep(more_or_less(second))



# helper functions with selenium base *********************************************************************
@contextmanager
def get_driver(**kwargs):
    try:
        driver = Driver(**kwargs)  # undetectable=True, incognito=True
        yield driver
    except:
        print('We had an error!')
    finally:
        driver.quit()
        print('Finished, driver quit.')



# helper functions with pyautogui ***************************************************************************

def locate_image_center_on_screen(image_file: str):
    assert Path(image_file).exists()
    try: 
        center = pyautogui.locateCenterOnScreen(image_file, grayscale=True) 
        return center
    except:
        return None

def perform_click(x, y) -> bool:
    try:
        # click
        pyautogui.moveTo(x, y, 2, pyautogui.easeInQuad) 
        pyautogui.click()
        print(f'clicked at {x}, {y}.')
        sleep(4)  # wait for web page to response
        # move out of the way to a random spot
        random_x = 200 + randint(1, 50)
        random_y = 300 + randint(1, 50)
        pyautogui.moveTo(random_x, random_y, 2, pyautogui.easeInQuad)
        return True
    except:
        return False


def start_pyautogui():
    """start pyautogui 
    NOTE: if remote interation is not enable yet need to mannually click on popup window to:
        allow remote interation and 
        share window
    """
    print(f'cursor initial position: {pyautogui.position()}')
    new_position = (281, 295)  # just a random position to stay out of the way
    pyautogui.moveTo(*new_position, 2, pyautogui.easeInQuad) 
    sleep(3)


def handle_verification() -> bool:
    """handle cloudflare verification"""
    checkbox_image = './images/checkbox-image.png'   
    assert Path(checkbox_image).exists()
    attempt = 0
    while attempt < 3:
        if target_center := locate_image_center_on_screen(checkbox_image):
            if perform_click(target_center.x, target_center.y):
                print('clicked checkbox.')
                sleep(4) # wait for page to refresh
                if not locate_image_center_on_screen(checkbox_image):
                    return True
        else:
            print('trying to locate checkbox...')
        attempt += 1
    return False 


