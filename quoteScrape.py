#Quote Scrape - Python3
#12th MArch 2017
import json
import urllib

import requests
from bs4 import BeautifulSoup
from lxml import html

print("+++ Quote Scrape +++ ")

URL_TOP_250 = 'http://www.imdb.com/chart/top'
OUTPUT_PATH = "quotes.json"

quotesDictList = []

def buildQuoteDict(filmName, quotes):
    quoteDict = {}
    quoteDict['Film'] = filmName
    quoteDict['Quotes'] = quotes

    return quoteDict

def outputToFile(quotesDictList):
    quoteFile = open(OUTPUT_PATH, 'w')
    json.dump(quotesDictList, quoteFile)
    quoteFile.close()

def getQuotesFrom(url):
    print("Getting Quotes")
    page = requests.get(url)
    tree = html.fromstring(page.content)

    filmName = tree.xpath('//*[@property="og:title"]/@content')[0]
    quotesList = tree.xpath('//*[@id="quotes_content"]/div[2]/div/div[@class="sodatext"]')

    formatted_quotes = []

    for quote in quotesList:
        formatted_quote_line = ''
        for quote_line in quote:
            formatted_quote_line += quote_line.text_content().strip().replace('\n', '') + '\n'
        formatted_quotes.append(formatted_quote_line.strip())

    quotesDictList.append(buildQuoteDict(filmName, formatted_quotes))


def get_movie_quotes_url(movie_id):
    return "http://www.imdb.com/title/" + movie_id + "/trivia?tab=qt&ref_=tt_trv_qu"

def retrieveMovieList(url):
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)

    movieList = soup.findAll("div", {"class": "seen-widget"})

    for movie in movieList:
        getQuotesFrom(get_movie_quotes_url(movie['data-titleid']))


retrieveMovieList(URL_TOP_250)

outputToFile(quotesDictList)

print("+++ Done +++")
