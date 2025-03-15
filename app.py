# python -m app


# NOTE: when encounter 'Xlib.error.DisplayConnectionError'
# in Linux terminal run: 'xhost +' 
# response: 'access control disabled, clients can connect from any host'

# NOTE: not able to handld cloudflare with builtin seleniumbase methods

# NOTE: not able to locate cloudflare iframe with driver.find_element

# NOTE: on Fedora, need Python 3.10 to be compatible with pyautogui and its dependencies

# NOTE: seems like pyautogui.locateCenterOnScreen prefer simple image with simple lines

# NOTE: As of pyautogui version 0.9.41, if the locate functions can’t find the provided image, 
# they’ll raise ImageNotFoundException instead of returning None.

# NOTE:
# with SB(undetected=True, incognito=True) as driver:
# with DriverContext(uc=True) as driver: 
# both these context managers seem not fully compatible with Fedora, 
# causing error: "X11 display failed! Will use regular xvfb!"

# NOTE: on Fedora, need the followings libs for pyautogui
# sudo dnf install scrot
# sudo dnf install python3-tkinter
# sudo dnf install python3-devel

# use pipenv to generate requirements.txt 
# pipenv run pip freeze > requirements.txt   


import random

from time import sleep
from pathlib import Path

from src import utils, pages, locators, selectors
from importlib import reload
reload(utils)  # make sure updates on utils funcs in effect
reload(pages)
reload(locators)
reload(selectors)


from src.utils import get_driver
from src.utils import (start_pyautogui, 
                       locate_image_center_on_screen, 
                       perform_click)


from src.locators import locator_input_job_title, locator_input_location, locator_find_job_button

from src.selectors import (TITLE, LOCATION, SUBMIT, REMOTE_FILTER, REMOTE, LANGUAGE_FILTER, LANGUAGE_MENU)



def more_or_less(number: int) -> float:
    sign = random.choice([1, -1])
    delta = random.randint(1, 100) / 1000
    return number * (1 + sign * delta)


def sleepy(second: int):
    sleep(more_or_less(second))


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


def main():
    start_pyautogui() 
    with get_driver(undetectable=True, incognito=True) as driver:  
        url = 'https://ca.indeed.com/'
        driver.uc_open_with_reconnect(url, 10)
        driver.maximize_window()
        sleepy(5) # wait long enough for the cloudflare checkbox to appear
        
        if not handle_verification():
            print('failed to handle cloudflare verification, exiting...')
            return
        sleepy(3)
        
        driver.type(TITLE, 'accountant')
        sleepy(2)
        driver.type(LOCATION, 'Vancouver, BC')
        sleepy(2)
        driver.click(SUBMIT)
        sleepy(10)

        # driver.click_link(link_text)



if __name__ == '__main__':
    main()
    
