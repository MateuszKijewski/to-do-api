import requests
import urllib.request
import sys

from bs4 import BeautifulSoup


url = "https://www.brainyquote.com/topics/inspirational-quotes"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
x = soup.find_all(title="view quote")
result=[]
for quote in x:
    result.append(quote.string)