

import random, string, os

from pathlib import Path

from bs4 import BeautifulSoup


folder = Path('./jobposts/')
assert folder.exists() and folder.is_dir()



def main():

    n = 0
    for file in folder.iterdir():
        if n > 0: break
        print(file.name)

        with open(file, 'r', encoding='utf-8') as html_file:
            soup = BeautifulSoup(html_file, 'html.parser')
            title = list(soup.css.select("h2[data-testid='simpler-jobTitle']"
                                         )[0].stripped_strings)
            print(f'Title: \n{title}')
            
            detail = list(soup.css.select("div[id='jobDetailsSection']"
                                          )[0].stripped_strings)
            print(f'Brief Detail: \n{detail}')
            
            # NOTE: some jobposts have not location section
            if location_soups := soup.css.select("div[id='jobLocationWrapper']"):
                location = list(location_soups[0].stripped_strings)
                print(f'Location: \n{location}')
            else:
                print('No Location Section.')

            # NOTE: some jobposts have not benefit section
            if benefit_soups := soup.css.select("div[id='benefits']"):
                benefit = list(benefit_soups[0].stripped_strings)
                print(benefit)
            else:
                print('no benefit section.')

            description = list(soup.css.select("div[id='jobDescriptionText']"
                                               )[0].stripped_strings)
            print(f'Job Description:\n {description}')
            

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

