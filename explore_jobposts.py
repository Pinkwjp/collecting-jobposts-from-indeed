

import random, string, os
from pathlib import Path
from typing import Union, List

from bs4 import BeautifulSoup


folder = Path('./jobposts/')
assert folder.exists() and folder.is_dir()




def extract_stripped_strings(soup: BeautifulSoup, css_selector: str) -> Union[List[str], None]:
    """assuming css_selector correspons to NO MORE THAN ONE element"""

    if sub_soups := soup.css.select(css_selector):
        return list(sub_soups[0].stripped_strings)  # 1 or none
    else:
        return None



def main():

    n = 0
    for file in folder.iterdir():
        # if n > 3: break
        print('****************************************************************************\n')

        print(f'File: {file.name}\n')

        with open(file, 'r', encoding='utf-8') as html_file:
            soup = BeautifulSoup(html_file, 'html.parser')
            title = list(soup.css.select("h2[data-testid='simpler-jobTitle']"
                                         )[0].stripped_strings)
            print(f'Title: \n{title}\n')
            
            # NOTE: some jobposts have not detail section
            # if detail_soups := soup.css.select("div[id='jobDetailsSection']"):
            #     detail = list(detail_soups[0].stripped_strings)
            #     print(f'Brief Detail: \n{detail}\n')
            # else:
            #     print('No Detail Section.\n')
            
            css_job_detail = "div[id='jobDetailsSection']"
            if detail := extract_stripped_strings(soup, css_job_detail):
                print(f'Brief Detail: \n{detail}\n')
            else:
                print(f'No --- {css_job_detail} --- found.\n')


            # NOTE: some jobposts have not location section
            if location_soups := soup.css.select("div[id='jobLocationWrapper']"):
                location = list(location_soups[0].stripped_strings)
                print(f'Location: \n{location}\n')
            else:
                print('No Location Section.\n')

            # NOTE: some jobposts have not benefit section
            if benefit_soups := soup.css.select("div[id='benefits']"):
                benefit = list(benefit_soups[0].stripped_strings)
                print(f'Benefit: \n{benefit}\n')
            else:
                print('no benefit section.')

            description = list(soup.css.select("div[id='jobDescriptionText']"
                                               )[0].stripped_strings)
            print(f'Job Description:\n {description}\n')

        print('****************************************************************************\n')
            

        n += 1




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
    print(f'removed {n} file in {folder.absolute()}.')
    


if __name__ == '__main__':
    # python -m explore_jobposts

    main()
    # make_empty_file(2)
    # remove_empty_file('./jobposts/')

