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

title = soup.find("span", itemprop="name").get_text()
print(title)

#type = soup.find('a', href="https://myanimelist.net/topanime.php?type=tv").getText()

linkdata = soup.select('a[href^="https://myanimelist.net/"]')
type = linkdata[40].text
print(type)

ref = soup.find("div", class_="spaceit")
episodes = ref.get_text()
episodes2 = episodes.rstrip()
numEp = episodes2[13:]
print(numEp)

ref2 = ref.find_next_sibling("div", class_="spaceit")
date = ref.find_next_sibling("div", class_="spaceit").get_text()
if len(date[10:17]) >= 6:
    airDate = date[18:22].rstrip()
else:
    airDate = date[17:22].rstrip()
print(airDate)

s = soup.select('a[href^="/anime/producer/"]')


ref3 = ref2.find_next_sibling("div", class_="spaceit")
ref4 = ref3.find_next_sibling("div", class_="spaceit")
ref5 = ref4.find_next_sibling("div", class_="spaceit")
#studios = ref5.find_next_sibling("div", class_="spaceit").getText()

print(s[0].text)