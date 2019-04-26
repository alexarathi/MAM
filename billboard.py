
from bs4 import BeautifulSoup
import requests
import os
import sqlite3

#Create 3 BeautifulSoup objects
url = 'https://www.billboard.com/charts/hot-100'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

url2 = 'https://www.billboard.com/charts/billboard-200'
r = requests.get(url2)
soup2 = BeautifulSoup(r.text, 'html.parser')

url3 = 'https://www.billboard.com/charts/dance-electronic-songs'
r = requests.get(url3)
soup3 = BeautifulSoup(r.text, 'html.parser')

#Creates a databse in sqlite called "billboard"
conn = sqlite3.connect('Billboard.sqlite')
cur = conn.cursor()

#Creates the first table in Billboard called Billboard
cur.execute('CREATE TABLE Billboard(artist TEXT, rank TEXT, song TEXT)')

#Finds all the div tags with the class "chart-list-item" within the billboard top 100
song = soup.find_all('div', class_ = 'chart-list-item')

#pulls data from the div tag and sorts them into variables 
for s in song:
    artist = (s["data-artist"])
    rank = (s["data-rank"])
    song = (s["data-title"])
    
    #Inserts values of artist, rank, and song into the table
    cur.execute('INSERT INTO Billboard (artist, rank, song) VALUES (?,?,?)', (artist, rank, song)) 

conn.commit()

#Creates the second table in Billboard called Billboard2
cur.execute('CREATE TABLE Billboard2(artist2 TEXT, rank2 TEXT, song2 TEXT)')

song2 = soup2.find_all('div', class_ = 'chart-list-item')

#pulls data from the div tag and sorts them into variables 
for s in song2:
    artist2 = (s["data-artist"])
    rank2 = (s["data-rank"])
    song2 = (s["data-title"])

    #Inserts values of artist, rank, and song into the table
    cur.execute('INSERT INTO Billboard2 (artist2, rank2, song2) VALUES (?,?,?)', (artist2, rank2, song2)) 
conn.commit()

#Creates the third table in Billboard called Billboard3
cur.execute('CREATE TABLE Billboard3(artist3 TEXT, rank3 TEXT, song3 TEXT)')

song3 = soup3.find_all('div', class_ = 'chart-list-item')

#pulls data from the div tag and sorts them into variables 
for s in song3:
    artist3 = (s["data-artist"])
    rank3 = (s["data-rank"])
    song3 = (s["data-title"])

    #Inserts values of artist, rank, and song into the table
    cur.execute('INSERT INTO Billboard3 (artist3, rank3, song3) VALUES (?,?,?)', (artist3, rank3, song3)) 

#commits the information
conn.commit()




conn.close()
