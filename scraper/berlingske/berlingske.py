
""" Scrape the media archives of the Berlingske newspaper.

The archive is structured by year and month, with each section containing a varying
number of "parts". Each of these parts contain a lot of articles.
"""

import requests
import random
import pandas as pd
from time import sleep, time
from bs4 import BeautifulSoup

BASE = 'https://www.b.dk'


def index_url(year, month):
    """ Create the base url for a given year and month
    """
    return f'{BASE}/artikel-arkiv/{year}/{month}'



def get(url, attempts=5, check_function=lambda x: x.ok):
    """ Tries to get the URL a set number of times, before assuming the link is
    broken
    """
    for iteration in range(attempts):
        try:
            # add ratelimit function call here
            sleep(2)

            t0 = time()
            response = requests.get(url)
            t1 = time()

            if t1 - t0 > 6:
                print(f"Sleeping for an additional {t1 - t0} seconds.")
                sleep(t1 - t0)

            if check_function(response):
                return response # if succesful it will end the iterations here
        except exceptions as e: #  find exceptions in the request library requests.exceptions
            print("An error occured. Did not get page.")
            print(e) # print or log the exception message.
    return None



def get_all_parts(url):
    """ Find links to all parts within a specific year, month
    """
    resp = get(url)
    if resp.ok:
        soup = BeautifulSoup(resp.text, 'lxml')
    parts = [url['href'] for url in soup.find('div', {'class':'col-lg-8 col-lg-offset-2'}).find_all('a') if 'del' in str(url)]
    return [BASE + p for p in parts]



def get_all_article_links(year, month, sample = False, samplefrac = None):
    """ Gets the links to all articles written in a specific month
    """
    url = index_url(year, month)
    parts = get_all_parts(url)
    article_links = []
    print(f"There are {len(parts)} parts in month {month} of {year}.")

    if sample:
        print(f"Sampling a share {samplefrac} of all avaliable parts")
        iter = random.sample(parts, round(len(parts)*samplefrac))
    else:
        iter = parts

    remaining = len(iter)

    for part in iter:
        print(f"Remaining {remaining} parts to retrieve.")
        articles = get(part)

        if articles is None:
            # We couldn't get the page
            continue

        soup = BeautifulSoup(articles.text, 'lxml')
        article_relative_paths = [url['href'] for url in soup.find('ul', {'class':'list-reset list-news list'}).find_all('a')]
        article_links += [BASE + link for link in article_relative_paths]
        remaining -= 1

    return article_links



def get_article_content(article_link):
    """ Get the content of a specific article
    """
    print(f"getting article {article_link}")
    page = get(article_link)
    soup = BeautifulSoup(page.text, 'lxml')

    try:
        headline = soup.find('h1', {'class': 'article-header__title'}).getText().strip()
    except:
        headline = None
    try:
        subhead = soup.find('p', {'class':'article-header__summary'}).getText().strip()
    except:
        subhead = None
    try:
        publishdate = soup.find('div', {'class': 'article-date'}).getText().strip().split('\n')[0]
    except:
        publishdate = None
    try:
        articlebody = '\n'.join([s.getText() for s in soup.find('div', {'class':'article-body'}).find_all('p')])
    except:
        articlebody = None
    try:
        author = soup.find('div', {'class': 'article-top__partner-byline'}).getText().strip()
    except:
        author = None

    return pd.DataFrame({'link': [article_link],
                         'headline': [headline],
                         'subhead': [subhead],
                         'publishdate': [publishdate],
                         'articlebody': [articlebody],
                         'author': [author]})



def get_all_content(year,
                    month,
                    sample_days = False, # Sample days in the month?
                    samplefrac_days = None,
                    sample_articles = False,  # Sample articles within each day?
                    samplefrac_articles = None
                    ):
    """ Get all media content from berlingske in a specified month and year.
    """
    print(" --- GETTING ARTICLE LINKS --- ")
    article_links = get_all_article_links(year, month, sample_days, samplefrac_days)
    print("Got all parts. Continuing.")

    i = 0
    fullset = get_article_content(article_links[0])

    if sample_articles:
        print(f"Sampling a share {samplefrac_articles} of all avaliable links")
        iter = random.sample(article_links[1:], round(len(article_links[1:])*samplefrac_articles))
    else:
        iter = article_links[1:]

    print(f"There are {len(iter)} articles to get in month {month} {year}.")
    for link in iter:
        fullset = pd.concat([fullset, get_article_content(link)])

        if i % 50 == 0 and i != 0:
            fullset.to_csv('berlingske.csv', index = False)
        i += 1

    fullset.to_csv('berlingske_final.csv', index = False)
    return fullset
