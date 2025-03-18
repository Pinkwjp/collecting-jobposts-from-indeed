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


from importlib import reload

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


from src import utils, pages, selectors
reload(utils)  # make sure updates on utils funcs in effect
reload(pages)
reload(selectors)

from src.utils import get_driver, sleepy
from src.utils import start_pyautogui, handle_verification
from src.selectors import (TITLE, LOCATION, SUBMIT, 
                           REMOTE_FILTER, REMOTE, HYDBRID,
                           LANGUAGE_FILTER)



def main():
    start_pyautogui() 
    with get_driver(undetectable=True, incognito=True) as driver:  
        url = 'https://ca.indeed.com/'
        driver.uc_open_with_reconnect(url, 10)
        sleepy(1)

        driver.maximize_window()
        sleepy(5) # wait long enough for the cloudflare checkbox to appear
        
        if not handle_verification():
            print('failed to handle cloudflare verification, exiting...')
            return
        sleepy(3)
        
        # search jobs
        driver.type(TITLE, 'accountant')  # lawyer
        sleepy(2)
        driver.type(LOCATION, 'Vancouver, BC')
        sleepy(2)
        driver.click(SUBMIT)
        sleepy(3)
        
        # filter jobs
        driver.click(REMOTE_FILTER)
        sleepy(0.5)
        driver.click(REMOTE)
        sleepy(3)

        driver.click(LANGUAGE_FILTER)
        sleepy(0.5)
        driver.click_link('English')
        sleepy(4)  # wait for page to full loaded
        # self.select_option_by_text(dropdown_selector, option, dropdown_by="css selector", timeout=None)
        
        job_beacons = driver.find_elements("div[class='job_seen_beacon']")  # div[id='mosaic-jobResults']
        if not job_beacons:
            print('cannot find job becons.')
            return
        else:
            print('find job becons.')
        sleepy(2)

        
        i = 0
        for beacon in job_beacons:
            beacon.click()
            print('click job beacon.')
            sleepy(2)

            # link_text_element = beacon.find_element(By.TAG_NAME, 'a')
            # if link_text_element:
            #     print(f'find link text element.')
            # else:
            #     print('cannot find link text element.')
            # sleepy(1)
            
            # if not link_text_element.get_attribute('aria-label'):
            #     print('not a valid job beacon, skipped.')
            #     continue

            # label = link_text_element.get_attribute('aria-label')
            # if label:
            #     print(f'find label: {label}')
            # else:
            #     print('cannot find label.')
            #     continue
            # sleepy(1)

            # id = link_text_element.get_attribute('id')
            # if id:
            #     print(f'find id: {id}')
            # else:
            #     print('cannot find id.')
            # sleepy(1)
            
            try:
                actions = ActionChains(driver)
                actions.move_to_element(beacon).click(beacon)  # scroll_to_element(beacon).
                print('performed actions move to and click element.')
                sleepy(2)
                
            except:
                print('something wrong with actions.')
            
            # div[id='jobsearch-ViewjobPaneWrapper']


            i += 1
            if i > 5: break


        sleepy(5)



if __name__ == '__main__':
    # python -m app
    main()
    
