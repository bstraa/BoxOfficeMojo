from bs4 import BeautifulSoup
from collections import defaultdict
import requests
import urlparse
import re
import pickle


def gen_list_of_urls(LETTERS, BASE_URL, SLUG):
    '''
    Returns a list of URLs (list_of_urls) which contain links to each individual movie webpage.
    '''
    list_of_urls = []
    for letter in LETTERS:
        for number in range(0,22):
            url = urlparse.urljoin(BASE_URL, SLUG.format(ltr=letter, pge=number))
            list_of_urls.append(url)
    return list_of_urls


def get_raw_html(list_of_urls, MOVIE_DICT):
    '''
    Returns a list of URLs (movie_url_list) which are the individual movie webpages by calling get_soup().
    '''
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
    '''
    Supporting function for get_raw_html()
    Builds dictionary using BeautifulSoup to scrape the links for each individual movie webpages.
    '''
    soup = BeautifulSoup(raw_html)
    for x in soup.find('div', {'id': 'body'}).find_all(href=re.compile('/movies/\?id')):
        try:
            x = str(x).split('="')
            x = x[1].split('">')
            sub_url = x[0]
            MOVIE_DICT[sub_url]
        except:
            pass


def pickle_urls(movie_url_list):
    with open('url_list.pkl', 'w') as picklefile:
        pickle.dump(movie_url_list, picklefile)


def main():
    '''
    Outputs a pickled list of individual movie URLs that are to be scraped for movie data.
    '''
    BASE_URL = 'http://www.boxofficemojo.com/'
    SLUG = 'movies/alphabetical.htm?letter={ltr}&page={pge}&p=.htm'
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    MOVIE_DICT = defaultdict(dict)
    list_of_urls = gen_list_of_urls(LETTERS, BASE_URL, SLUG)
    movie_url_list = get_raw_html(list_of_urls, MOVIE_DICT)
    pickle_urls(movie_url_list)


if __name__ == '__main__':
    main()
