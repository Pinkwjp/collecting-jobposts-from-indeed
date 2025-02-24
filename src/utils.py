from time import sleep
from contextlib import contextmanager
from pathlib import Path

from seleniumbase import Driver
import pyautogui



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


def click_checkbox_on_verification_page() -> bool:
    checkbox_image = './images/checkbox.png' 
    assert Path(checkbox_image).exists()
    checkbox_center = locate_image_center_on_screen(checkbox_image)
    if checkbox_center:
        pyautogui.moveTo(checkbox_center.x, checkbox_center.y, 2, pyautogui.easeInQuad) 
        pyautogui.click()
        print('clicked checkbox')
        sleep(4)  # wait for web page to response
        pyautogui.moveTo(223, 323, 2, pyautogui.easeInQuad) # move away from the clicked object 
        pyautogui.click()
        sleep(4)  # wait for web page to response
        return True
    else:
        return False


def at_target_page() -> bool:
    image_on_target_page = './images/email-field-dark.png' # screen partially black out by the cookies setting popup
    assert Path(image_on_target_page).exists()
    if locate_image_center_on_screen(image_on_target_page):
        return True
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

