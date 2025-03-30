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

from src import utils, selectors
reload(utils)  
reload(selectors)

from src.utils import get_driver, slow_down
from src.utils import start_pyautogui 

from src.collector import Collector



def main():
    download_folder = './jobposts/'
    if not Path(download_folder).exists():
        Path.mkdir(download_folder)
    assert Path(download_folder).is_dir()

    start_pyautogui() 
    with get_driver(undetectable=True, incognito=True) as driver:  
        collector = Collector(driver, 'https://ca.indeed.com/')
        collector.open_webpage()   #  cybersecurity, accountant, software engineer, 
        collector.search_jobs(job_title='software engineer', job_location='Montreal, QC')  # Toronto, ON  Montreal, QC  Vancouver, BC
        collector.filter_remote_jobs('remote')
        collector.filter_job_language('English')
        collector.collect_jobposts(download_folder, n=5)
        slow_down(8)


if __name__ == '__main__':
    # python -m app
    main()
    

