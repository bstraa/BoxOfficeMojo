# standard imports
from collections import defaultdict
import pickle
import re
import requests
import urllib.parse

# 3rd party imports
from bs4 import BeautifulSoup


def gen_list_of_urls(letter_string, base_string, slug_string):
    """
    Generate a list of URL's to scrape.
    """
    list_of_urls = []
    for letter in letter_string:
        for number in range(0, 22):
            url = urllib.parse.urljoin(
                base_string,
                slug_string.format(ltr=letter, pge=number),
            )
            list_of_urls.append(url)
    return list_of_urls


def get_raw_html(list_of_urls, movie_set):
    """
    Scrape list of URL's to generate new list of URL's.
    """
    movie_url_list = []  # non-complete English sentence
    for url in list_of_urls:
        response = requests.get(url)
        if response.ok:
            raw_html = response.text
            get_soup(raw_html, movie_set)
        else:
            print('response error')
    movie_url_list = list(MOVIE_DICT)
    return movie_url_list


def get_soup(raw_html, movie_set):
    """
    Supporting function for get_raw_html() which retrieves URL's using BS.
    """
    soup = BeautifulSoup(raw_html, 'lxml')
    for x in soup.find('div', {'id': 'body'}).find_all(href=re.compile('/movies/\?id')):
        try:
            x = str(x).split('="')
            x = x[1].split('">')
            sub_url = x[0]
            movie_set[sub_url]
        except:
            pass


def pickle_urls(movie_url_list):
    # Pickles URL's
    with open('url_list2.pkl', 'wb') as picklefile:
        pickle.dump(movie_url_list, picklefile)


def main():
    """
    Outputs a pickled list of individual movie URLs that are to be scraped
    for movie data.
    """
    BASE_URL = 'http://www.boxofficemojo.com/'
    SLUG = 'movies/alphabetical.htm?letter={ltr}&page={pge}&p=.htm'
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    MOVIE_SET = set()
    list_of_urls = gen_list_of_urls(LETTERS, BASE_URL, SLUG)
    movie_url_list = get_raw_html(list_of_urls, MOVIE_SET)
    pickle_urls(movie_url_list)


if __name__ == '__main__':
    main()
