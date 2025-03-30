
from importlib import reload
import random, string, os
from pathlib import Path
from typing import Union, List

from bs4 import BeautifulSoup

from src import selectors
reload(selectors)
from src.selectors import (JOB_DETAILS, JOB_BENEFIT, JOB_TITLE, JOB_DESCRIPTION, JOB_LOCATION)





def extract_stripped_strings(soup: BeautifulSoup, css_selector: str) -> Union[List[str], None]:
    """assuming css_selector correspons to NO MORE THAN ONE element"""

    if sub_soups := soup.css.select(css_selector):
        return list(sub_soups[0].stripped_strings)  # 1 or none
    else:
        print(f'No --- {css_selector} --- found.\n')
        return None


def make_empty_file(n:int = 1):
    folder = Path('./jobposts/')
    assert folder.is_dir()
    for _ in range(n):
        file_name = ''.join(random.choices(population=string.digits + string.ascii_lowercase, 
                                        k=10)
                            ) + '.html'
        with open(folder / file_name, mode='x') as f:
            pass 


def remove_empty_file(folder_path: str) -> None:
    folder = Path(folder_path)
    assert folder.exists() and folder.is_dir()
    n = 0
    for file in folder.iterdir():
        if os.stat(file).st_size == 0:
            os.remove(file) 
            n += 1
    print(f'removed {n} empty file in {folder.absolute()}.')
    

def main():
    folder = Path('./jobposts/')
    assert folder.exists() and folder.is_dir()

    for i, file in enumerate(folder.iterdir()):
        if i > 2: break
        print('*' * 100, '\n')
        print(f'File: {file.name}\n')
        with open(file, 'r', encoding='utf-8') as html_file:
            soup = BeautifulSoup(html_file, 'html.parser')

            print(f'Title: \n{extract_stripped_strings(soup, JOB_TITLE)}\n')
            
            if details := extract_stripped_strings(soup, JOB_DETAILS):  # NOTE: some jobposts have not detail section
                print(f'Brief Detail: \n{details}\n')

            if location := extract_stripped_strings(soup, JOB_LOCATION):  # NOTE: some jobposts have not location section
                print(f'Location: \n{location}\n')

            if benefit := extract_stripped_strings(soup, JOB_BENEFIT):  # NOTE: some jobposts have not benefit section
                print(f'Benefit: \n{benefit}\n')

            print(f'Job Description:\n {extract_stripped_strings(soup, JOB_DESCRIPTION)}\n')
            
        print('*' * 100, '\n')



if __name__ == '__main__':
    # python -m explore_jobposts

    remove_empty_file('./jobposts/')
    main()
    # make_empty_file(2)
    



