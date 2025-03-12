# python3 src/page_objects/locators.py
# locators for WebElement


from typing import Callable



class Locator:
    
    def __init__(self, css_selector):
        self.css_selector = css_selector



# basic search
locator_input_job_title = Locator(css_selector="input[id='text-input-what']")
locator_input_location = Locator(css_selector="input[id='text-input-where']")
locator_find_job_button = Locator(css_selector="button[type='submit']")



# # google sign-in iframe popup
# IFRAME_GOOGLE_SIGN_IN = Locator(strategy=By.CSS_SELECTOR, 
#                                 value="iframe[title='Sign in with Google Dialog']",
#                                 expected_condition=EC.frame_to_be_available_and_switch_to_it)
# CLOSE_BUTTON_GOOGLE_SIGN_IN = Locator(strategy=By.ID, value='close')  # NOTE: only valid after driver locate and switch to iframe 

# # cloudflare iframe popup
# IFRAME_CLOUDFLARE = Locator(strategy=By.CSS_SELECTOR,
#                             value="iframe[title='Widget containing a Cloudflare security challenge']")
# CLOUDFLARE_CHECKOBX = Locator(strategy=By.CSS_SELECTOR,
#                               value="input [type='checkbox']")


# # remote filter on search result page
# BUTTON_REMOTE = Locator(strategy=By.ID, value='remote_filter_button')  #FIXME: remote_filter_button
# DROPDOWN_MENU_REMOTE = Locator(By.CSS_SELECTOR,                       # NOTE: only valid after remote button is clicked (visible)
#                                value="div[aria-labelledby='remote_filter_button']", #
#                                                                        #old value: "ul[id='filter-remotejob-menu']"
#                                expected_condition=EC.visibility_of_element_located)

# MENU_ITEM = Locator(By.CSS_SELECTOR, value="a[role='menuitem']")
# #TODO:  maybe MENU_ITEM = Locator(By.TAG_NAME, value="a") #  for all filter dropdown menu

# # job language filter on search result page
# BUTTON_JOB_LANGUAGE = Locator(strategy=By.ID, value='filter-lang')
# DROPDOWN_MENU_JOB_LANGUAGE = Locator(By.CSS_SELECTOR, value="ul[id='filter-lang-menu']")
# JOB_LANGUAGE_ITEM = Locator(By.TAG_NAME, value="a")  


# # search result page navigation
# PAGE_NAVIGATION = Locator(strategy=By.CSS_SELECTOR, 
#                           value="nav[role='navigation'] ul",
#                           expected_condition=EC.element_to_be_clickable)
# PAGE_NAVIGATION_ITEM = Locator(By.TAG_NAME, "a")


# # job cards on search result page
# JOB_CARDS = Locator(strategy=By.CSS_SELECTOR, value="div[id='mosaic-jobResults']")  # multiple (up to around 15) job cards  per page 
# JOB_CARD = Locator(strategy=By.CSS_SELECTOR, value="ul li table[role='presentation']")  # individual job card


# # the only one full job description present in current page, corresponds to the expand full job detail, default to the first job post)
# JOB_FULL_DETAIL = Locator(strategy=By.CSS_SELECTOR, value="div[id='jobsearch-ViewjobPaneWrapper']") # NOTE: only vaild in search result page



if __name__ == '__main__':
    pass 
