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

# TODO:
# create a class based on Driver to overwrite find_elements() and find_element() for better error handling

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
        driver.type(TITLE, 'java developer')  # lawyer, accountant, software developer
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
        
        # find all job beacons on current page
        job_beacons = driver.find_elements("div[class='job_seen_beacon']")  
        if not job_beacons:
            print('cannot find job becons.')
            return
        else:
            print('find job becons.')
        sleepy(2)

        # click and expand job descriptions
        i = 0
        for beacon in job_beacons:
            beacon.click() # somehow need this to make ActionChains function properly
            print('click job beacon.')
            sleepy(1)

            try:
                actions = ActionChains(driver)
                actions.move_to_element(beacon).click(beacon)  # scroll_to_element(beacon).
                print('performed actions: move to and click element.')
                sleepy(3)
                
                job_detail = driver.find_element("div[id='jobsearch-ViewjobPaneWrapper']")  # will raise error if cannot find target
                if job_detail:
                    print('find job detail.')
                else:
                    print('cannot find job detail.')
                sleepy(1)
                
                id = beacon.find_element(By.TAG_NAME,'a').get_attribute('id')
                
                # with open('workfile', encoding="utf-8") as f:
                try:
                    with open(f'./jobposts/{id}.html', 'w', encoding='utf-8') as f:
                        f.write(job_detail.get_attribute('innerHTML'))
                        print(f'saved jobpost {id}.')
                except Exception as e:
                    print(f'when trying to save jobpost, this error happended: {e}')

            except:
                print('something wrong with actions.')
            
            i += 1
            if i > 3: break
        print()

        # go to next page
        try:
            # driver.scroll_to_bottom() # not working

            current_url = driver.get_current_url()

            next_page_button = driver.find_element("a[data-testid='pagination-page-next']") # will raise error if cannot find target
            next_page_button.click()
            print('clicked next page')
            sleepy(3)

            new_url = driver.get_current_url()
            if current_url != new_url:
                print('arrived at next page.')
            

            # move_to_element_with_offset

            
            # if not next_page_button:
            #     print('cannot find next page button.')
            # else:
            #     print('found next page button')
            #     current_url = driver.get_current_url()
            #     ActionChains(driver).move_to_element(next_page_button).click(next_page_button)
            #     print('clicked next page')
            #     sleepy(3)
            #     new_url = driver.get_current_url()
            #     if current_url != new_url:
            #         print('arrived at next page.')
        except:
            print('cannot find next page button.')


        sleepy(8)



if __name__ == '__main__':
    # python -m app
    main()
    