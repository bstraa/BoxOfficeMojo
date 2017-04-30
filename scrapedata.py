# standard imports
from collections import defaultdict
import re
import pickle
import requests

# 3rd party imports
from bs4 import BeautifulSoup


def get_raw_html_movie(base_string, slug_string, movie_dict, movie_list):
    """
    Inputs the list of individual movie webpage URL's and calls BeautifulSoup
    scraping function get_soup_again() to pull data.  Then calls pickle
    function to output defaultdict(dict).
    """
    counter = 0     #Created counter to guage progress.
    for slug in movie_list:
        if counter % 500 == 0:
            print(movie_dict[movie_list[counter-1]])
            print('Processing Movie #%d' % counter)
        counter += 1
        try:
            response = requests.get(base_string + slug + slug_string)
            if response.ok:
                raw_html_movie = response.text
                get_soup_again(raw_html_movie, slug, movie_dict)
            else:
                print('Response Error')
        except:
            pass
    outpickle(movie_dict)


def get_soup_again(raw_html_movie, movie_url, movie_dict):
    """
    Supporting scraping function called by get_raw_html_movie() to pull
    appropriate data using BeautifulSoup.
    """
    soup_again = BeautifulSoup(raw_html_movie, 'lxml')
    try:
        for y in soup_again.find('div', {'class': 'mp_box_content'}):
            try:
                foreign = y.find_all('td')[4].text
                movie_dict[movie_url]['foreign'] = foreign
            except:
                pass
        for x in soup_again.find('div', {'id': 'body'}).find('table').find_all('table')[3]:
            try:
                dom = x.find('td').find('tr').find('font').find('b').text
                dist = x.find_all('td')[2].find('a').text
                release = x.find_all('td')[3].find('a').text
                genre = x.find_all('td')[4].find('b').text
                runtime = x.find_all('td')[5].find('b').text
                rating = x.find_all('td')[6].find('b').text
                budget = x.find_all('td')[7].find('b').text
                movie_dict[movie_url]['domestic'] = dom
                movie_dict[movie_url]['distributor'] = dist
                movie_dict[movie_url]['release'] = release
                movie_dict[movie_url]['genre'] = genre
                movie_dict[movie_url]['runtime'] = runtime
                movie_dict[movie_url]['rating'] = rating
                movie_dict[movie_url]['budget'] = budget
            except:
                pass
    except:
        pass


def outpickle(slug_dict):
    with open('all_movie_data5.pkl', 'wb') as outpick:
        print(slug_dict)
        pickle.dump(slug_dict, outpick)


def inpickle(filename):
    with open(filename, 'rb') as inpick:
        url_list = pickle.load(inpick)
        return url_list


def main():
    """
    Opens the pickled list of URLs to scrape created by scrapeurls.py.  Pulls
     data using BeautifulSoup and outputs a pickled defaultdict(dict).
    """
    BASE_URL = 'http://www.boxofficemojo.com'
    SLUG_URL = '&adjust_yr=2017&p=.htm'
    PICKLEFILE = 'url_list4.pkl'
    PICKLEFILE2 = 'movie_data2.pkl'
    MOVIE_LIST = inpickle(PICKLEFILE)
    MOVIE_DICT = inpickle(PICKLEFILE2)
    get_raw_html_movie(BASE_URL, SLUG_URL, MOVIE_DICT, MOVIE_LIST)


if __name__ == '__main__':
    main()
