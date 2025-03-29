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
from pathlib import Path

from seleniumbase import Driver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


from src import utils, pages, selectors
reload(utils)  
reload(pages)
reload(selectors)

from src.utils import get_driver, slow_down
from src.utils import start_pyautogui, handle_verification
from src.selectors import (SEARCH_TITLE, SEARCH_LOCATION, SEARCH_SUBMIT, 
                           REMOTE_FILTER, REMOTE, HYDBRID, NEXT_PAGE,
                           LANGUAGE_FILTER, JOB_BEACON, FULL_JOB_DETAIL)



class Collector:

    def __init__(self, driver: Driver, url: str) -> None:
        self.driver = driver
        self.url = url
    
    def open_webpage(self) -> None:
        self.driver.uc_open_with_reconnect(self.url, 10)
        slow_down(2)
        self.driver.maximize_window()
        slow_down(5) # wait long enough for the cloudflare checkbox to appear
        handle_verification()
        slow_down(1)

    def search_jobs(self, job_title: str, job_location: str) -> None:
        self.driver.type(SEARCH_TITLE, job_title)  
        slow_down(2)
        self.driver.type(SEARCH_LOCATION, job_location)
        slow_down(2)
        self.driver.click(SEARCH_SUBMIT)
        slow_down(3)

    def filter_jobs(self) -> None:
        self.driver.click(REMOTE_FILTER)
        slow_down(0.5)
        self.driver.click(REMOTE)
        slow_down(3)
        self.driver.click(LANGUAGE_FILTER)
        slow_down(0.5)
        self.driver.click_link('English')
        slow_down(5)  # wait for page to full loaded
    
    def _expand_job_description(self, job_beacon) -> None:
        job_beacon.click()  # somehow need this to make ActionChains function properly
        slow_down(2)
        print('click job beacon.')

        actions = ActionChains(self.driver)
        actions.move_to_element(job_beacon).click(job_beacon)  # to make job post shown on screen
        print('performed actions: move to and click element.')
        slow_down(3)
    
    
    def _download_full_job_detail(self, folder, job_beacon) -> None:
        """download the currently expanded job description"""
        job_id = job_beacon.find_element(By.TAG_NAME,'a').get_attribute('id')
        full_job_detail = self.driver.find_element(FULL_JOB_DETAIL)  # will raise error if cannot find target
        with open(f'{folder}/{job_id}.html', 'w', encoding='utf-8') as f:
            f.write(full_job_detail.get_attribute('innerHTML'))
            print(f'saved jobpost {job_id}.')


    def collect_jobposts(self, folder: str) -> None:
        # find all job beacons on current page
        assert Path(folder).exists() and Path(folder).is_dir()

        job_beacons = self.driver.find_elements(JOB_BEACON)  
        for i, job_beacon in enumerate(job_beacons):
            slow_down(2)
            self._expand_job_description(job_beacon)
            self._download_full_job_detail(folder, job_beacon)
            
            if i > 2: break


    def go_to_next_page(self) -> bool:
        try:
            url = self.driver.get_current_url()
            self.driver.find_element(NEXT_PAGE).click()
            print('clicked next page button')
            slow_down(3)
            if url != self.driver.get_current_url():
                print('arrived at next page.')
            return True
        except:
            print('error: failed to go to next page.')
            return False





def main():
    start_pyautogui() 
    with get_driver(undetectable=True, incognito=True) as driver:  
        url = 'https://ca.indeed.com/'
        driver.uc_open_with_reconnect(url, 10)
        slow_down(1)

        driver.maximize_window()
        slow_down(5) # wait long enough for the cloudflare checkbox to appear
        
        if not handle_verification():
            print('failed to handle cloudflare verification, exiting...')
            return
        slow_down(3)
        
        # search jobs
        driver.type(SEARCH_TITLE, 'accountant')  # lawyer, accountant, software developer, java developer
        slow_down(2)
        driver.type(SEARCH_LOCATION, 'Vancouver, BC')
        slow_down(2)
        driver.click(SEARCH_SUBMIT)
        slow_down(3)
        
        # filter jobs
        driver.click(REMOTE_FILTER)
        slow_down(0.5)
        driver.click(REMOTE)
        slow_down(3)
        driver.click(LANGUAGE_FILTER)
        slow_down(0.5)
        driver.click_link('English')
        slow_down(4)  # wait for page to full loaded
        


        # find all job beacons on current page
        job_beacons = driver.find_elements("div[class='job_seen_beacon']")  
        if not job_beacons:
            print('cannot find job becons.')
            return
        else:
            print('find job becons.')
        slow_down(2)

        # click and expand job descriptions
        i = 0
        for beacon in job_beacons:
            beacon.click() # somehow need this to make ActionChains function properly
            print('click job beacon.')
            slow_down(1)

            try:
                actions = ActionChains(driver)
                actions.move_to_element(beacon).click(beacon)  # scroll_to_element(beacon).
                print('performed actions: move to and click element.')
                slow_down(3)
                
                job_detail = driver.find_element("div[id='jobsearch-ViewjobPaneWrapper']")  # will raise error if cannot find target
                if job_detail:
                    print('find job detail.')
                else:
                    print('cannot find job detail.')
                slow_down(1)
                
                id = beacon.find_element(By.TAG_NAME,'a').get_attribute('id')
                
                # with open('workfile', encoding="utf-8") as f:
                try:
                    with open(f'./jobposts/mar-24/{id}.html', 'w', encoding='utf-8') as f:
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
            slow_down(3)

            new_url = driver.get_current_url()
            if current_url != new_url:
                print('arrived at next page.')
            

            # move_to_element_with_offset
            # scroll_to_element

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


        slow_down(8)





def main_x():
    download_folder = './jobposts/test/'
    assert Path(download_folder).exists() and Path(download_folder).is_dir()

    start_pyautogui() 
    with get_driver(undetectable=True, incognito=True) as driver:  
        collector = Collector(driver, 'https://ca.indeed.com/')
        collector.open_webpage()
        collector.search_jobs(job_title='cybersecurity', job_location='Toronto, ON') # cybersecurity, accountant,  
        # collector.filter_jobs()
        collector.collect_jobposts(folder=download_folder)
        collector.go_to_next_page()
        slow_down(8)



if __name__ == '__main__':
    # python -m app

    # main()
    main_x()


    