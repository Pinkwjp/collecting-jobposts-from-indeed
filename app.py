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

from src import utils, selectors, collector
reload(utils)  
reload(selectors)
reload(collector)

from src.utils import get_driver, slow_down
from src.utils import start_pyautogui 
from src.collector import Collector



def main():
    download_folder = './jobposts/remote/'
    if not Path(download_folder).exists():
        Path(download_folder).mkdir(parents=True)
    assert Path(download_folder).is_dir()

    start_pyautogui() 
    with get_driver(undetectable=True, incognito=True) as driver:  
        collector = Collector(driver, 'https://ca.indeed.com/', 
                              job_id_db_path='./jobposts/id_to_filename_db')  # './jobposts/jobpost_id_to_filename.json'
        collector.open_webpage()   #  'cybersecurity', 'accountant', 'sales person', 'civil engineer'
        for title in ['python', 'data science']:  #  , 'software engineer', 'software developer', 'machine learning'
            for city in ['Toronto, ON']:  # 'Montreal, QC',  , 'Vancouver, BC'
                collector.search_jobs(job_title=title, job_location=city)  
                collector.filter_remote_jobs('remote')
                collector.filter_job_language('English')
                n_collected = collector.collect_jobposts(download_folder, n=2)
                print(f'OK, collected {n_collected} {title} related jobposts in {city}.')
                slow_down(8)





if __name__ == '__main__':
    # python -m app
    main()
    



