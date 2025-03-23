

import random, string, os

from pathlib import Path

from bs4 import BeautifulSoup


folder = Path('./jobposts/')
assert folder.exists() and folder.is_dir()



def main():

    n = 0
    for file in folder.iterdir():
        if n > 1: break
        print(file.name)

        with open(file, 'r', encoding='utf-8') as html_file:
            soup = BeautifulSoup(html_file, 'html.parser')

            # title = [h2 for h2 in soup.find_all('h2') if (h2.get('data-testid') == 'simpler-jobTitle')][0].get_text()

            title = soup.css.select("h2[data-testid='simpler-jobTitle']")[0].get_text()
            print(f'job title: {title}')
            print()
            
            # find(name, attrs, recursive, string, **kwargs)
            # soup.css.select('a[href$="tillie"]')
            
            detail = soup.css.select("div[id='jobDetailsSection']")[0].get_text(separator=' | ')
            print(detail)
            print()
            
            # NOTE: some jobposts have not location section
            location_list = soup.css.select("div[id='jobLocationWrapper']")
            if location_list:
                location = location_list[0].get_text(separator=' | ')
                print(location)
                print()
            else:
                print('no location section.')
            print()

            # NOTE: some jobposts have not benefit section
            benefit_list = soup.css.select("div[id='benefits']")
            if benefit_list:
                location = benefit_list[0].get_text(separator=' | ')
                print(location)
            else:
                print('no benefit section.')
            print()

            description = soup.css.select("div[id='jobDescriptionText']")[0].get_text(separator=' | ')
            print(f'job description: {description}')
            print()
            

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

