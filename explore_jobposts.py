
from pathlib import Path

from bs4 import BeautifulSoup


folder = Path('./jobposts/')
assert folder.exists() and folder.is_dir()


def main():
    for file in folder.iterdir():
        with open(file, 'r', encoding='utf-8') as html_file:
            soup = BeautifulSoup(html_file, 'html.parser')
            # h2[data-testid='simpler-jobTitle']
            h2_title = filter(lambda tag: tag.attrs.get('data-testid') == 'simpler-jobTitle', soup.find_all('h2'))
            print(f'job title: {h2_title.string}')



if __name__ == '__main__':
    # python -m explore_jobposts
    main()