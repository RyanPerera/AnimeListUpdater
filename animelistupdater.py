# To parse Anime series information from HTML page and use to update a spreadsheet
# By Ryan Perera, 2020

# Import libraries
import requests
import urllib.request
import time
import re
from bs4 import BeautifulSoup

# Set the URL you want to webscrape from
url = 'https://myanimelist.net/anime/9314/Fractale'

# Connect to the URL
response = requests.get(url)

# Parse HTML and save to BeautifulSoup object¶
soup = BeautifulSoup(response.text, "html.parser")

# Title
title = soup.find("span", itemprop="name").get_text()
print(title)

# Type
linkdata = soup.select('a[href^="https://myanimelist.net/"]')
type = linkdata[40].text
print(type)

# Number of Episodes
ref = soup.find("div", class_="spaceit")
episodes = ref.get_text()
episodes2 = episodes.rstrip()
numEp = episodes2[13:]
print(numEp)

# Duration
ref3 = ref2.find_next_sibling("div", class_="spaceit")
ref4 = ref3.find_next_sibling("div", class_="spaceit")
ref5 = ref4.find_next_sibling("div", class_="spaceit")
ref6 = ref5.find_next_sibling("div", class_="spaceit")
duration = re.sub("[^0-9]", "", ref6.text)
print(duration)

# Date Released
ref2 = ref.find_next_sibling("div", class_="spaceit")
date = ref.find_next_sibling("div", class_="spaceit").get_text()
if len(date[10:17]) >= 6:
    airDate = date[18:22].rstrip()
else:
    airDate = date[17:22].rstrip()
print(airDate)

# Studios
divs = soup.select("div")
studios = divs[41].text.replace("Studios:", "").split(',')
for studio in studios:
    print(studio.lstrip().rstrip())

# Genres
genres = soup.select('a[href^="/anime/genre/"]')
for x in genres:
    print(x.text)




