# src/page_objects/elements.py

# some custom page element classes wrapping around Selenium WebElement


from time import sleep
from typing import Union, List, Callable

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from src.locators import Locator
from src.utils import handle_exceptions


class JobCard:
    """a helper class wraps around the jobcard WebElement"""

    name = 'JobCard'

    def __init__(self, element: WebElement) -> None:
        self.element = element
        self.link = self._find_link()
        self.job_id = self.link.get_attribute('id')
        self.data_mobtk = self.link.get_attribute('data-mobtk')
        self.data_jk = self.link.get_attribute('data-jk')
        self.href = self.link.get_attribute('href')
        assert self.job_id
    
    def link_info(self) -> dict:
        return {'id': self.job_id, 
                'data-jk': self.data_jk,
                'data-mobtk': self.data_mobtk,
                'href': self.href}
    
    def _find_link(self) -> WebElement:
        return self.element.find_element(by=By.CSS_SELECTOR, 
                                        value="a[role='button']")

    def get_job_id(self) -> str:
        return self.job_id
    
    def _find_job_id(self) -> Union[str, None]:
        return self.element.find_element(by=By.CSS_SELECTOR, 
                                        value="a[role='button']"
                                        ).get_attribute('id')
    
    def _find_data_mobtk(self) -> Union[str, None]:
        return self.element.find_element(by=By.CSS_SELECTOR, 
                                        value="a[role='button']"
                                        ).get_attribute('data-mobtk')
    
    def _find_data_jk(self) -> Union[str, None]:
        return self.element.find_element(by=By.CSS_SELECTOR, 
                                        value="a[role='button']"
                                        ).get_attribute('data-jk')
    # data-jk


    def expand_job_description(self) -> None:
        self.element.click()
        sleep(1.5)


class MyBaseElement:
    def __init__(self, page, name: str, locator: Locator) -> None:
        """
        page - the page object containing the element
        name - the name of the element
        locator - the locator for the element 
        """
        self.page = page 
        self.name = name
        self.locator = locator
        self.element = self._locate_element()
        sleep(1)

    def _locate_element(self) -> WebElement:
        return self.page.driver.find_element(self.locator.css_selector)  # seleniumbase driver


class InputElement(MyBaseElement):
    def __init__(self, page, name: str, locator: Locator) -> None:
        super().__init__(page, name, locator)
    
    def set_value(self, value: str):
        """set input field to value"""
        self.element.clear()
        self.element.send_keys(value)
        sleep(1)

    def get_value(self) -> str:   
        """return value of the input field"""
        return self.element.get_attribute('value')


class ButtonElement(MyBaseElement):
    def __init__(self, page, name: str, locator: Locator) -> None:
        super().__init__(page, name, locator)

    def click(self):
        """click button"""
        self.element.click()
        sleep(1.5)






class UnorderedList(MyBaseElement):
    """a class for ul (unordered list) elements"""

    def __init__(self, page, name: str, locator: Locator, item_locator: Locator) -> None:
        super().__init__(page, name, locator)
        self.item_locator = item_locator
        self.items = self._find_list_items() 
        sleep(1)
    
    @handle_exceptions
    def _find_list_items(self, ) -> List[WebElement]:
        """find the direct nesting list items"""
        return WebDriverWait(self.page.driver, 6
                             ).until(lambda x: self.element.find_elements(
                                 self.item_locator.strategy, self.item_locator.value)) 
    

class Menu(UnorderedList):
    
    def __init__(self, page, name: str, locator: Locator, item_locator: Locator) -> None:
        super().__init__(page, name, locator, item_locator)
        self.labels = self._find_labels()
        assert len(self.items) == len(self.labels)
        assert all(self.labels)

    def _find_labels(self) -> List[str]:
        """find the text or label for all the list items"""
        labels = []
        for item in self.items:
            if item.text:
                label = item.text.lower()
            elif item.get_attribute('aria-label'):
                label = item.get_attribute('aria-label').lower()
            else:
                label = ''
            labels.append(label)
        return labels
    
    def click_item_with_substring(self, substring: str) -> bool:
        for label, item in zip(self.labels, self.items):
            if substring in label:
                item.click()
                sleep(2)
                return True
        else:
            raise ValueError(f"No menu item contains substring {substring}.")


