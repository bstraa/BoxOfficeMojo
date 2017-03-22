from bs4 import BeautifulSoup
from collections import defaultdict
import requests
import urllib.parse
import re
import pickle


def gen_list_of_urls(LETTERS, BASE_URL, SLUG):
    list_of_urls = []
    for letter in LETTERS:
        for number in range(0,3):
            #3 was 22
            url = urllib.parse.urljoin(BASE_URL, SLUG.format(ltr=letter, pge=number))
            list_of_urls.append(url)
    return list_of_urls


def get_raw_html(list_of_urls, MOVIE_DICT):
    movie_url_list = []
    for url in list_of_urls:
        response = requests.get(url)
        if response.ok:
            raw_html = response.text
            get_soup(raw_html, MOVIE_DICT)
        else:
            print('response error')
    movie_url_list = MOVIE_DICT.keys()
    return movie_url_list



def get_soup(raw_html, MOVIE_DICT):
    soup = BeautifulSoup(raw_html, 'lxml')
    for x in soup.find('div', {'id': 'body'}).find_all(href=re.compile('/movies/\?id')):
        try:
            x = str(x).split('="')
            x = x[1].split('">')
            sub_url = x[0]
            MOVIE_DICT[sub_url]
        except:
            pass


def main():
    BASE_URL = 'http://www.boxofficemojo.com/'
    SLUG = 'movies/alphabetical.htm?letter={ltr}&page={pge}&p=.htm'
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    MOVIE_DICT = defaultdict(dict)
    list_of_urls = gen_list_of_urls(LETTERS, BASE_URL, SLUG)
    movie_url_list = get_raw_html(list_of_urls, MOVIE_DICT)
    print(movie_url_list)


if __name__ == '__main__':
    main()
