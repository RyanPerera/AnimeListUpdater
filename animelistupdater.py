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
from tkinter import *
from tkinter.ttk import *

window = Tk()

window.title("Anime List Updater")
window.geometry('700x100')
can = Canvas(window, height=100, width=700, highlightthickness = 0)
can.place(relx=0.5, rely=0.5, anchor=CENTER)
lbl = Label(can, text="Enter MyAnimeList URL:")
lbl.grid(column=0, row=0)
txt = Entry(can, width=70, state=NORMAL)
txt.grid(column=0,row=1)
txt.focus()
lblscr = Label(can, text="Score:")
lblscr.grid(column=1, row=0)
txtscr = Entry(can, width=3)
txtscr.grid(column=1,row=1)
lblsts = Label(can, text="Status:")
lblsts.grid(column=2, row=0)
combo = Combobox(can)
combo['value'] = ("To Watch", "In Progress", "Completed", "Dropped")
combo.current(0)
combo.grid(column=2, row=1)

def update(event=None):
    url = txt.get()
    status = combo.get()
    score = txtscr.get()

    # Connect to the URL
    response = requests.get(url)

    # Parse HTML and save to BeautifulSoup object
    soup = BeautifulSoup(response.text, "html.parser")

    #print("Parsing data...")

    # Title
    title = soup.find("span", itemprop="name").get_text()
    # print(title)

    # Type
    type = soup.select('a[href^="https://myanimelist.net/topanime.php?type="]')
    # print(type[0].text)

    # Number of Episodes
    ref = soup.find("div", class_="spaceit")
    episodes = ref.get_text()
    episodes2 = episodes.rstrip()
    numEp = episodes2[13:]
    # print(numEp)

    # Duration
    durationref = soup.find(text='Rating:').find_parent().find_previous().find_previous().find_parent()
    durationpre = re.sub("[^0-9]", "", durationref.text)
    if len(durationpre) > 2:
        duration = (int(durationpre[0]) * 60) + int(durationpre[1:])
    else:
        duration = int(durationpre)
    # print(duration)

    # Date Released
    date = ref.find_next_sibling("div", class_="spaceit").get_text()
    if "," not in date[10:16]:
        airDate = date[18:22].rstrip()
    else:
        airDate = date[17:22].rstrip()
    # print(airDate)

    # Studios
    studio1 = soup.find(text='Studios:').find_next()
    studio2 = studio1.find_next()
    # print(studio1.text)
    # print(studio2.text)

    # Genres
    genres = soup.select('a[href^="/anime/genre/"]')
    genrelistpre = ""
    for x in genres:
        genrelistpre += x.text + ", "
    genrelist = genrelistpre.rstrip(', ')
    # print(genrelist)

    #print("Finished parsing data!")
    
    #print("Updating Anime List...")

    # Authorize Google Drive/Sheets API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('venv\client_secret.json', scope)
    client = gspread.authorize(creds)

    # Open Workbook + sheet no.
    sheet = client.open("Anime List").sheet1

    # Get index of last empty row
    rowNum = str(len(sheet.get_all_values()) + 1)

    # Update worksheet
    sheet.append_row(
        [type[0].text, title, status, "Not Yet Rated", "0", numEp, duration, airDate, "-", "", "", genrelist,
         "=PRODUCT(E" + rowNum + ",G" + rowNum + ")"], value_input_option='USER_ENTERED')
    sheet.update_cell(rowNum, 10, studio1.text)
    if "Source:" not in studio2.text:
        sheet.update_cell(rowNum, 11, studio2.text)
    if len(score) != 0:
        sheet.update_cell(rowNum, 4, score)

    #print("Anime List Updated!")
    #print("Complete!")
    lbl.configure(text="Successfully updated. Send another?")
    txt.delete(0, END)


btn = Button(can, text="Update", command = update)
window.bind('<Return>', update)
btn.grid(column=0, row=5, padx=10, pady = 10)

window.mainloop()


















