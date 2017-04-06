# Quote Scrape - Python3
import json
import urllib

import requests
from bs4 import BeautifulSoup
from lxml import html

print("+++ Quote Scrape +++ ")

URL_TOP_250 = 'http://www.imdb.com/chart/top'
OUTPUT_PATH = "quotes.json"

quotesDictList = []


def build_quote_dict(film_name, quotes):
    quote_dict = {'Film': film_name, 'Quotes': quotes}

    return quote_dict


def output_to_file(quotes_dict_list):
    quote_file = open(OUTPUT_PATH, 'w')
    json.dump(quotes_dict_list, quote_file)
    quote_file.close()


def get_quotes_from(url):
    print("Getting Quotes")
    page = requests.get(url)
    tree = html.fromstring(page.content)

    film_name = tree.xpath('//*[@property="og:title"]/@content')[0]
    quotes_list = tree.xpath('//*[@id="quotes_content"]/div[2]/div/div[@class="sodatext"]')

    formatted_quotes = []

    for quote in quotes_list:
        formatted_quote_line = ''
        for quote_line in quote:
            formatted_quote_line += quote_line.text_content().strip().replace('\n', '') + '\n'
        formatted_quotes.append(formatted_quote_line.strip())

    quotesDictList.append(build_quote_dict(film_name, formatted_quotes))


def get_movie_quotes_url(movie_id):
    return "http://www.imdb.com/title/" + movie_id + "/trivia?tab=qt&ref_=tt_trv_qu"


def retrieve_movie_list(url):
    response = urllib.request.urlopen(url)
    html_full_page = response.read()
    soup = BeautifulSoup(html_full_page)

    movie_list = soup.findAll("div", {"class": "seen-widget"})

    for movie in movie_list:
        get_quotes_from(get_movie_quotes_url(movie['data-titleid']))


retrieve_movie_list(URL_TOP_250)

output_to_file(quotesDictList)

print("+++ Done +++")
