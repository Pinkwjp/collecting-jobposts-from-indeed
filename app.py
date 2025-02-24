# python -m app

from time import sleep

from src import utils
from importlib import reload
reload(utils)  # make sure updates on utils funcs in effect

from src.utils import get_driver
from src.utils import (start_pyautogui, at_target_page, 
                       click_checkbox_on_verification_page)





def main():
    start_pyautogui() 
    with get_driver(undetectable=True, incognito=True) as driver:  
        url = 'https://ca.indeed.com/'
        driver.uc_open_with_reconnect(url, 10)
        driver.maximize_window()
        sleep(5) # wait long enough for the cloudflare checkbox to appear
        attempt = 0
        while attempt < 3:
            if click_checkbox_on_verification_page():
                if at_target_page():
                    print('bypass verification, at target page!')
                    break
            else:
                print('failed to click checkbox.')
            attempt += 1



if __name__ == '__main__':
    main()
