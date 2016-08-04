from bs4 import BeautifulSoup
from collections import defaultdict
import requests
import urlparse
import re
import pickle


def get_raw_html_movie(BASE_URL, movie_list, MOVIE_DICT):
    '''
    Inputs the list of individual movie webpage URL's and calls BeautifulSoup scraping function get_soup_again() to pull data.  Then calls pickle function to output defaultdict(dict).
    '''
    #Created counter to guage progress.
    counter = 0
    for movie_url in movie_list:
        if counter % 500 == 0:
            print 'Processing Movie #%d' % counter
        counter += 1
        try:
            response = requests.get(BASE_URL + movie_url)
            if response.ok:
                raw_html_movie = response.text
                get_soup_again(raw_html_movie, movie_url, MOVIE_DICT)
            else:
                print('Response Error')
        except:
            pass
    outpickle(MOVIE_DICT)


def get_soup_again(raw_html_movie, movie_url, MOVIE_DICT):
    '''
    Supporting scraping function called by get_raw_html_movie() to pull appropriate data using BeautifulSoup.
    '''
    soup_again = BeautifulSoup(raw_html_movie)
    try:
        for y in soup_again.find('div', {'class': 'mp_box_content'}):
            try:
                foreign = y.find_all('td')[4].text
                MOVIE_DICT[movie_url]['foreign'] = foreign
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
                MOVIE_DICT[movie_url]['domestic'] = dom
                MOVIE_DICT[movie_url]['distributor'] = dist
                MOVIE_DICT[movie_url]['release'] = release
                MOVIE_DICT[movie_url]['genre'] = genre
                MOVIE_DICT[movie_url]['runtime'] = runtime
                MOVIE_DICT[movie_url]['rating'] = rating
                MOVIE_DICT[movie_url]['budget'] = budget
            except:
                pass
    except:
        pass


def outpickle(MOVIE_DICT):
    with open('all_movie_data.pkl', 'w') as outpick:
        pickle.dump(MOVIE_DICT, outpick)


def inpickle(PICKLEFILE):
    with open('url_list.pkl', 'r') as inpick:
        url_list = pickle.load(inpick)
        return url_list


def main():
    '''
    Opens the pickled list of URLs to scrape created by scrapeurls.py.  Pulls data using BeautifulSoup and outputs a pickled defaultdict(dict).
    '''
    BASE_URL = 'http://www.boxofficemojo.com/'
    PICKLEFILE = 'url_list.pkl'
    MOVIE_DICT = defaultdict(dict)
    url_list = inpickle(PICKLEFILE)
    get_raw_html_movie(BASE_URL, url_list, MOVIE_DICT)


if __name__ == '__main__':
    main()
