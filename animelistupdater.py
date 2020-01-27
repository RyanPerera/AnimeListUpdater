# To parse Anime series information from HTML page and use to update a spreadsheet
# https://docs.google.com/spreadsheets/d/17MIiMByf0udGcUZbb6q7UUgfrCF7PQH0Nd6_AAGvesA/edit#gid=0
# By Ryan Perera, 2020

# Import libraries
import requests
import urllib.request
import time
import re
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set the URL you want to webscrape from
url = input("Enter URL")

# Connect to the URL
response = requests.get(url)

# Parse HTML and save to BeautifulSoup object¶
soup = BeautifulSoup(response.text, "html.parser")

print("Parsing data...")

# Title
title = soup.find("span", itemprop="name").get_text()
#print(title)

# Type
type = soup.select('a[href^="https://myanimelist.net/topanime.php?type="]')
#print(type[0].text)

# Number of Episodes
ref = soup.find("div", class_="spaceit")
episodes = ref.get_text()
episodes2 = episodes.rstrip()
numEp = episodes2[13:]
#print(numEp)

# Duration
ref2 = ref.find_next_sibling("div", class_="spaceit")
ref3 = ref2.find_next_sibling("div", class_="spaceit")
ref4 = ref3.find_next_sibling("div", class_="spaceit")
ref5 = ref4.find_next_sibling("div", class_="spaceit")
ref6 = ref5.find_next_sibling("div", class_="spaceit")
duration = re.sub("[^0-9]", "", ref6.text)
#print(duration)

# Date Released
date = ref.find_next_sibling("div", class_="spaceit").get_text()
if "," not in date[10:16]:
    airDate = date[18:22].rstrip()
else:
    airDate = date[17:22].rstrip()
#print(airDate)

# Studios
studioref = ref4.find_next_sibling().text
studios = studioref.replace("Studios:", "").split(',')
#for studio in studios:
#    print(studio.lstrip().rstrip())

# Genres
genres = soup.select('a[href^="/anime/genre/"]')
genrelistpre = ""
for x in genres:
    genrelistpre += x.text + ", "
genrelist = genrelistpre.rstrip(', ')
#print(genrelist)

print("Finished parsing data!")
print("Updating Anime List...")

# Authorize Google Drive/Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('venv\client_secret.json', scope)
client = gspread.authorize(creds)

# Open Workbook + sheet no.
sheet = client.open("Anime List").sheet1

# Get index of last empty row
rowNum = str(len(sheet.get_all_values())+1)

# Update worksheet
sheet.append_row([type[0].text, title, "To Watch", "Not Yet Rated", "0", numEp, duration, airDate, "-", "" , "" , genrelist, "=PRODUCT(E" + rowNum +",G" + rowNum + ")"], value_input_option='USER_ENTERED')
sheet.update_cell(rowNum, 10, studios[0].lstrip().rstrip())
if (len(studios) > 1):
    sheet.update_cell(rowNum, 11, studios[1].lstrip().rstrip())
print("Anime List Updated!")
print("Complete!")


















