
from bs4 import BeautifulSoup
import requests
import os
import sqlite3

#Create BeautifulSoup objects!
url = 'https://www.billboard.com/charts/hot-100'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

url2 = 'https://www.billboard.com/charts/billboard-200'
r = requests.get(url2)
soup2 = BeautifulSoup(r.text, 'html.parser')

url3 = 'https://www.billboard.com/charts/dance-electronic-songs'
r = requests.get(url3)
soup3 = BeautifulSoup(r.text, 'html.parser')

#list of tags that contain our song information
conn = sqlite3.connect('Billboard.sqlite')
cur = conn.cursor()

cur.execute('CREATE TABLE Billboard(artist TEXT, rank TEXT, song TEXT)')

song = soup.find_all('div', class_ = 'chart-list-item')

for s in song:
    artist = (s["data-artist"])
    rank = (s["data-rank"])
    song = (s["data-title"])
        
    cur.execute('INSERT INTO Billboard (artist, rank, song) VALUES (?,?,?)', (artist, rank, song)) 

conn.commit()

cur.execute('CREATE TABLE Billboard2(artist2 TEXT, rank2 TEXT, song2 TEXT)')

song2 = soup2.find_all('div', class_ = 'chart-list-item')

for s in song2:
    artist2 = (s["data-artist"])
    rank2 = (s["data-rank"])
    song2 = (s["data-title"])

    cur.execute('INSERT INTO Billboard2 (artist2, rank2, song2) VALUES (?,?,?)', (artist2, rank2, song2)) 
conn.commit()

cur.execute('CREATE TABLE Billboard3(artist3 TEXT, rank3 TEXT, song3 TEXT)')

song3 = soup3.find_all('div', class_ = 'chart-list-item')

for s in song3:
    artist3 = (s["data-artist"])
    rank3 = (s["data-rank"])
    song3 = (s["data-title"])

    cur.execute('INSERT INTO Billboard3 (artist3, rank3, song3) VALUES (?,?,?)', (artist3, rank3, song3)) 

conn.commit()




conn.close()
