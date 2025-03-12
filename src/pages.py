


from time import sleep
from typing import List, Dict
from pathlib import Path

from src import locators, elements

from importlib import reload

reload(locators)
reload(elements)

from src.elements import MyBaseElement, InputElement, ButtonElement, UnorderedList, Menu, JobCard




class BasePage:   
    def __init__(self, url: str,  driver: WebDriver):  # type hinting enable autocomplete in code editor
        self.url = url
        self.driver = driver
        self.driver.get(self.url)
        self.driver.maximize_window()
        sleep(2)  # NOTE: important, wait for page to load the google sign-in request

 


class XPage:   

    def __init__(self, driver):
        self.driver = driver
        self._input_job_title = InputElement(page=self, name='input_job_title', locator=locators.INPUT_TITLE_KEYWORDS_COMPANAY) 
        self._input_job_location = InputElement(page=self, name='input_job_location', locator=locators.INPUT_LOCATION)
        self._find_jobs_button = ButtonElement(page=self, name='find_jobs_button', locator=locators.BUTTON_FIND_JOB)
    
    def search_jobs(self, title: str, location: str = "Toronto, ON"):
        self._input_job_title.set_value(title)
        self._input_job_location.set_value(location)
        self._find_jobs_button.click() 
        sleep(5)









class Page(BasePage):   

    def __init__(self, url: str, driver: WebDriver):
        super().__init__(url, driver)
        sleep(5)
        # self.handle_cloudflare()
        # sleep(2)
        # self.handle_google_sign_in_iframe() 

        # turn these into cached property
        self.input_field_job_title = InputElement(page=self, name='input_field_job_title', locator=locators.INPUT_TITLE_KEYWORDS_COMPANAY) 
        self.input_field_job_location = InputElement(page=self, name='input_field_job_location', locator=locators.INPUT_LOCATION)
        self._find_jobs_button = ButtonElement(page=self, name='_find_jobs_button', locator=locators.BUTTON_FIND_JOB)
    
    def search_jobs(self, what_job: str, where_job: str = "Toronto, ON"):
        """perform Indeed home page job search"""
        self.input_field_job_title.set_value(what_job)
        self.input_field_job_location.set_value(where_job)
        self._find_jobs_button.click() 
        sleep(2)
        # self.handle_cloudflare()
    
    # def handle_cloudflare(self):
    #     try:
    #         cloudflare_iframe = MyBaseElement(page=self, name='cloudflare_iframe', locator=locators.IFRAME_CLOUDFLARE)
    #         # self.driver.switch_to.frame(cloudflare_iframe.element)
    #         checkbox = InputElement(page=self, name='cloudflare_checkbox', locator=locators.CLOUDFLARE_CHECKOBX)
    #         checkbox.element.click()
    #         sleep(2)
    #         # self.driver.switch_to.default_content()
    #     except:
    #         print('notice: did not find any cloudflare iframe!')

    def handle_google_sign_in_iframe(self):
        google_iframe = MyBaseElement(page=self, name='google_iframe', locator=locators.IFRAME_GOOGLE_SIGN_IN)  # locate and switch to iframe
        close_button = ButtonElement(page=self, name='google_iframe_close_button', locator=locators.CLOSE_BUTTON_GOOGLE_SIGN_IN)  # find close button witin iframe
        close_button.click()
        self.driver.switch_to.default_content()  

    def is_in_search_results_page(self) -> bool:
        sleep(1)
        return 'jobs' in self.driver.title.lower()
    
    # TODO: dropdown button and dropdown menu cound bundle together:  button -> click -> dropdown
    def filter_remote_jobs(self):
        assert self.is_in_search_results_page()
        ButtonElement(page=self, name='remote_button', locator=locators.BUTTON_REMOTE).click() # expand the dropdown menu
        remote_dropdown_menu = Menu(page=self,   # NOTE: only work after expanding the dropdown (visible)
                                    name='remote_dropdown_menu',
                                    locator=locators.DROPDOWN_MENU_REMOTE, 
                                    item_locator=locators.MENU_ITEM)
        remote_dropdown_menu.click_item_with_substring('remote')
        self.handle_job_alert_popup()  # NOTE: a job alert popup after filtering remote job posts

    def filter_job_language(self, language: str = 'english'):
        # assert self.is_in_search_results_page()
        ButtonElement(page=self, name='job_language_button', locator=locators.BUTTON_JOB_LANGUAGE).click()  # expand the dropdown menu
        job_language_dropdown_menu = Menu(page=self,   # NOTE: only work after expanding the dropdown (visible)
                                          name='job_language_dropdown_menu',
                                          locator=locators.DROPDOWN_MENU_JOB_LANGUAGE,
                                          item_locator=locators.JOB_LANGUAGE_ITEM)
        job_language_dropdown_menu.click_item_with_substring(language)

    def handle_job_alert_popup(self):
        element = self.driver.switch_to.active_element  # switch to popup
        sleep(2)
        element.click()
        self.driver.switch_to.default_content()
    
    # TODO: refactor, add suppress
    def go_to_next_result_page(self) -> bool:
        # assert self.is_in_search_results_page()
        try:
            page_navigation = Menu(page=self, 
                                   name='page_navigation',
                                    locator=locators.PAGE_NAVIGATION, 
                                    item_locator=locators.PAGE_NAVIGATION_ITEM)
        except TimeoutException as e:
            print('NOTE: cannot find page navigation panel, ' 
                  'maybe there is only one page job search results.'
                  f'\nAdditional info: {e.msg}')
            return False
        else:
            return page_navigation.click_item_with_substring('next') 

    def get_job_cards(self) -> List[JobCard]:
        # assert self.is_in_search_results_page()
        job_card_ul = UnorderedList(page=self, 
                                    name='job_card_ul',
                                     locator=locators.JOB_CARDS, 
                                     item_locator=locators.JOB_CARD)
        return [JobCard(element=item) for item in job_card_ul.items]
    
    # def new_get_job_cards(self):
    #     assert self.is_in_search_results_page()
    #     job_card_ul = UnorderedList(page=self, 
    #                                 name='job_card_ul',
    #                                  locator=locators.JOB_CARDS, 
    #                                  item_locator=locators.JOB_CARD)
    #     return job_card_ul

    def _save_job_description(self, output_file: Path) -> None:
        """assuming there is a full job description present in current page"""
        with open(output_file, 'w+', encoding='utf-8') as file:
            file.write(MyBaseElement(page=self, 
                                     name='job_description',
                                       locator=locators.JOB_FULL_DETAIL
                                       ).element.get_attribute('innerHTML'))

    def collect_job_posts(self, folder: Path, job_id_to_link_dict: Dict) -> int:
        """collect job posts presented on current job results page
        
        return the number of job post collected
        """
        assert self.is_in_search_results_page()
        num = 0
        for job_card in self.get_job_cards():
            if (id := job_card.get_job_id()) in job_id_to_link_dict:  # skip collected job post
                continue
            job_card.expand_job_description()                  # NOTE: expand job description will trigger url change
            job_id_to_link_dict[id] = self.driver.current_url  # update db 
            self._save_job_description(output_file=folder/f'{id}.html')
            num += 1
        return num
    
    def new_collect_job_posts(self, job_id_to_link_dict: Dict) -> int:
        """collect job posts presented on current job results page
        
        return the number of job post collected
        """
        # assert self.is_in_search_results_page()
        num = 0
        for job_card in self.get_job_cards():
            link_info = job_card.link_info()
            if (id := link_info['id']) in job_id_to_link_dict:  # skip collected job post
                continue
            # job_card.expand_job_description()                  # NOTE: expand job description will trigger url change
            job_id_to_link_dict[id] = link_info  # update db 
            # self._save_job_description(output_file=folder/f'{id}.html')
            num += 1
        return num

