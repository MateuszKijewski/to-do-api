import requests
import urllib.request
import sys
import json

from bs4 import BeautifulSoup


def inspirational_quotes_scraper():
    """Scrapes inspirational quotes from BrainyQuote"""

    urls = [
        "https://www.brainyquote.com/topics/work-quotes",
        "https://www.brainyquote.com/topics/failure-quotes",
        "https://www.brainyquote.com/topics/succes-quotes"
    ]
    quotes = []
    authors = []

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        scraped_quotes = soup.find_all(title="view quote")
        scraped_authors = soup.find_all(title="view author")


        for quote, author in zip(scraped_quotes, scraped_authors):
            quotes.append(quote.string)
            authors.append(author.string)



    quotes = json.dumps(quotes)
    authors = json.dumps(authors)

    return (quotes, authors)