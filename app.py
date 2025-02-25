# python -m app

from time import sleep
from pathlib import Path

from src import utils
from importlib import reload
reload(utils)  # make sure updates on utils funcs in effect

from src.utils import get_driver
from src.utils import (start_pyautogui, 
                       locate_image_center_on_screen, 
                       perform_click)



def handle_verification() -> bool:
    # assume at Indeed home page with cloudflare verification
    checkbox_image = './images/checkbox.png' 
    assert Path(checkbox_image).exists()
    attempt = 0
    while attempt < 3:
        if target_center := locate_image_center_on_screen(checkbox_image):
            if perform_click(target_center.x, target_center.y):
                print('clicked checkbox.')
                sleep(4) # wait for page to refresh
                if not locate_image_center_on_screen(checkbox_image):
                    print('bypass verification!')
                    return True
        else:
            print('cannot to locate checkbox.')
        attempt += 1
    print('failed to bypass verification.')
    return False 


def main_x():
    start_pyautogui() 
    with get_driver(undetectable=True, incognito=True) as driver:  
        url = 'https://ca.indeed.com/'
        driver.uc_open_with_reconnect(url, 10)
        driver.maximize_window()
        sleep(5) # wait long enough for the cloudflare checkbox to appear

        if not handle_verification():
            print('exiting...')
        
        print('ok') 





def main():
    start_pyautogui() 
    with get_driver(undetectable=True, incognito=True) as driver:  
        url = 'https://ca.indeed.com/'
        driver.uc_open_with_reconnect(url, 10)
        driver.maximize_window()
        sleep(5) # wait long enough for the cloudflare checkbox to appear

        checkbox_image = './images/checkbox.png' 
        assert Path(checkbox_image).exists()
        attempt = 0
        while attempt < 3:
            if target_center := locate_image_center_on_screen(checkbox_image):
                if perform_click(target_center.x, target_center.y):
                    print('clicked checkbox.')
                    sleep(4) # wait for page to refresh
                    if not locate_image_center_on_screen(checkbox_image):
                        print('bypass verification!')
                        break
            else:
                print('failed to locate checkbox.')
            attempt += 1



if __name__ == '__main__':
    # main()
    main_x()

