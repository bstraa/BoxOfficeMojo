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
        url = urllib.parse.urljoin(
            base_string,
            slug_string.format(ltr=letter),
        )
        list_of_urls.append(url)
    return list_of_urls


def update_list_of_urls(list_of_urls):
    """
    Iterate through generic list of URLs and scrape additional ones.
    """
    updated_list_of_urls = []
    for url in list_of_urls:
        response = requests.get(url)
        if response.ok:
            raw_html = response.text.encode('unicode_escape')
            soup = BeautifulSoup(raw_html, 'lxml')
            num_pages = len(soup.find('div', {'class': 'alpha-nav-holder'}).find_all('b'))
            for num in range(1, num_pages+1):
                supporting_url = '&page={page_num}&p=.htm'.format(page_num=num)
                updated_list_of_urls.append(url+supporting_url)
    return updated_list_of_urls


def get_raw_html(list_of_all_urls, movie_container):
    """
    Scrape list of URL's to generate new list of URL's.
    """
    for url in list_of_all_urls:
        response = requests.get(url)
        if response.ok:
            raw_html = response.text
            get_soup(raw_html, movie_container)
        else:
            print('response error')
    movie_url_list = list(movie_container.keys())
    return movie_url_list, movie_container


def get_soup(raw_html, movie_container):
    """
    Supporting function for get_raw_html() which retrieves URL's using BS.
    """
    soup = BeautifulSoup(raw_html, 'lxml')
    for x in soup.find('div', {'id': 'body'}).find_all('table')[3].find_all('tr')[1:]:
        try:
            link = x.find('a')['href']
            title = x.find('a').text
            num_open_theatres = x.find_all('font')[5].text
            print(link, title, num_open_theatres)
            movie_container[link]['title'] = title
            movie_container[link]['num_open_theatres'] = num_open_theatres
        except:
            pass


def pickle_urls(movie_url_list, movie_container):
    with open('url_list4.pkl', 'wb') as picklefile:
        print(len(movie_url_list))
        pickle.dump(movie_url_list, picklefile)
    with open('movie_data2.pkl', 'wb') as picklefile2:
        print(movie_container)
        pickle.dump(movie_container, picklefile2)


def main():
    """
    Outputs a pickled list of individual movie URLs that are to be scraped
    for movie data.
    """
    BASE_URL = 'http://www.boxofficemojo.com/'
    SLUG = 'movies/alphabetical.htm?letter={ltr}'
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    MOVIE_CONTAINER = defaultdict(dict)
    list_of_urls = gen_list_of_urls(LETTERS, BASE_URL, SLUG)
    list_of_all_urls = update_list_of_urls(list_of_urls)
    movie_url_list, movi_container = get_raw_html(list_of_all_urls, MOVIE_CONTAINER)
    pickle_urls(movie_url_list, movi_container)


if __name__ == '__main__':
    main()
