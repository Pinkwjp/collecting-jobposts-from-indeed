
from importlib import reload
from typing import Union
import shelve

from seleniumbase import Driver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


from src import utils, selectors
reload(utils)  
reload(selectors)

from src.utils import slow_down, handle_verification
from src.selectors import (SEARCH_TITLE, SEARCH_LOCATION, SEARCH_SUBMIT, 
                           REMOTE_FILTER, NEXT_PAGE,
                           LANGUAGE_FILTER, JOB_BEACON, FULL_JOB_DETAIL)


from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
 


class Collector:

    def __init__(self, driver: Driver, url: str, job_id_db_path: str) -> None:
        self.driver = driver
        self.url = url
        # assert Path(job_id_db_path).exists() and Path(job_id_db_path).suffix == '.json'
        self.db = job_id_db_path
    
    def open_webpage(self) -> None:
        self.driver.uc_open_with_reconnect(self.url, 10)
        slow_down(2)
        self.driver.maximize_window()
        slow_down(5) # wait long enough for the cloudflare checkbox to appear
        handle_verification()
        slow_down(1)
    
    def _clear_and_type(self, input_element_css: str, text: str) -> None:
        element = self.driver.find_element(input_element_css)
        assert element
        # clear input field
        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.click(element)  # activate input field
        actions.double_click(element)  # double click to selecet all text
        actions.send_keys(Keys.BACKSPACE)  # delete selected text
        actions.perform()
        slow_down(0.5)
        assert not element.get_attribute('value')  # verify input field is clear
        # type text
        self.driver.type(input_element_css, text)  

    def search_jobs(self, job_title: str, job_location: str) -> None:
        self._clear_and_type(input_element_css=SEARCH_TITLE, text=job_title)
        slow_down(1)
        self._clear_and_type(input_element_css=SEARCH_LOCATION, text=job_location)
        slow_down(1)
        self.driver.click(SEARCH_SUBMIT)
        slow_down(3)
    
    def _filter_jobs(self, menu_css_selector: str, option: str) -> None:
        try:
            self.driver.click(menu_css_selector)
            slow_down(0.5)
            self.driver.click_link(option)
            slow_down(3)
        except:
            print(f'error: failed to filter {option} jobs.')

    def filter_remote_jobs(self, remote_option:str = '') -> None:
        """remote or hybrid"""
        if remote_option.lower() == 'remote':
            self._filter_jobs(menu_css_selector=REMOTE_FILTER, 
                              option='Remote')
        elif remote_option.lower() == 'hybrid':  # Hybrid work
            self._filter_jobs(menu_css_selector=REMOTE_FILTER, 
                              option='Hybrid work')
        else:
            print(f'error: {remote_option} is not a valid remote options.')
    
    def filter_job_language(self, language_option:str = '') -> None:
        """English or French"""
        if language_option.lower() == 'english':
            self._filter_jobs(menu_css_selector=LANGUAGE_FILTER,
                              option='English')
        elif language_option.lower() == 'french':
            self._filter_jobs(menu_css_selector=LANGUAGE_FILTER,
                              option='Français')
        else:
            print(f'error: {language_option} is not a valid language options.')

    def _expand_job_description(self, job_beacon) -> None:
        job_beacon.click()  # somehow need this to make ActionChains function properly
        slow_down(1.2)
        print('click job beacon.')
        actions = ActionChains(self.driver)
        actions.move_to_element(job_beacon).click(job_beacon)  # to make job post shown on screen
        print('performed actions: move to and click element.')
        slow_down(2.2)
    
    def _download_full_job_detail(self, folder: str, job_beacon: WebElement) -> None:
        """download the currently expanded job description"""
        try:
            job_id = job_beacon.find_element(By.TAG_NAME,'a').get_attribute('id')
            full_job_detail = self.driver.find_element(FULL_JOB_DETAIL)  # will raise error if cannot find target
            with open(f'{folder}/{job_id}.html', 'w', encoding='utf-8') as f:
                f.write(full_job_detail.get_attribute('innerHTML'))
                print(f'saved jobpost {job_id}.')
        except:
            print(f'error: something went wrong when tring to save jobpost {job_id}.')

    def _go_to_next_page(self) -> bool:
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
    
    def _is_in_db(self, job_id: str) -> bool:
        try:
            with shelve.open(self.db) as db:
                if job_id in db: 
                    print(f'jobpost {job_id} already in db.')
                    return True
                else:
                    return False
        except:
            print('error when trying to open db.')
    
    def _add_to_db(self, job_id: str) -> None:
        try:
            with shelve.open(self.db) as db:
                db[job_id] = f'{job_id}.html'
                print(f'add {job_id} to db.') 
        except:
            print('error when trying to open db.')

    def collect_jobposts(self, folder: str, n: Union[int, None] = None) -> int:
        count = 0
        while (n is None) or (count <= n):
            job_beacons = self.driver.find_elements(JOB_BEACON)  
            for job_beacon in job_beacons:
                job_id = job_beacon.find_element(By.TAG_NAME,'a').get_attribute('id')
                
                if self._is_in_db(job_id): 
                    continue
                self._add_to_db(job_id)    
                slow_down(2)
                self._expand_job_description(job_beacon)
                self._download_full_job_detail(folder, job_beacon)
                count += 1
                if count == n:
                    break
                    
            if (count == n) or (not self._go_to_next_page()):
                # print(f'collected {count} jobposts.')
                return count






