

import random, string, os

from pathlib import Path
from typing import Union

from bs4 import BeautifulSoup


folder = Path('./jobposts/')
assert folder.exists() and folder.is_dir()


# import os
# 

# TODO:
# add f to delete emtpy file on jobposts folder


def main():
    for file in folder.iterdir():
        print(file.name)
        with open(file, 'r', encoding='utf-8') as html_file:
            soup = BeautifulSoup(html_file, 'html.parser')
            # h2[data-testid='simpler-jobTitle']
            
            # tag.attrs

            
            title = [h2 for h2 in soup.find_all('h2') if (h2.get('data-testid') == 'simpler-jobTitle')]

            print(title)
            print()
            # get_text()
            # assert h2_title
            # print(f'job title: {h2_title.string}')


            # h2_list = soup.find_all('h2')
            # for h2 in h2_list:
            #     if h2.get('data-testid') == 'simpler-jobTitle':
            #         print(f'found job title: {h2.string}')
            #     print(h2.string)



def check_it():
    file = folder / 'job_d02570b8d2917f73.html'  # jobposts/job_d02570b8d2917f73.html
    assert file.exists()
    with open(file, 'r', encoding='utf-8') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')

        title = [h2 for h2 in soup.find_all('h2') if (h2.get('data-testid') == 'simpler-jobTitle')][0].get_text()
        print(f'found job title: {title}')

        # h2_list = soup.find_all('h2')
        # for h2 in h2_list:
        #         if h2.get('data-testid') == 'simpler-jobTitle':
                    
        #         print(h2.string)

        # print(soup.prettify())


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

    # check_it()
    # main()
    # make_empty_file(2)
    remove_empty_file('./jobposts/')

