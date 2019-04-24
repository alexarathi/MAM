from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re
import sqlite3


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://en.wikipedia.org/wiki/"
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")

conn = sqlite3.connect('SIProject.sqlite')
cur = conn.cursor()





def getartistURL(artist):
    new_url = "https://en.wikipedia.org/wiki/"
    '''if "Featuring" in artist:
        actual_artist = artist.split("Featuring")[0]
        if "&" in artist:
            actual_artist = actual_artist.split("&")[0]
            if "X" in artist.lower():
                actual_artist = actual_artist.split("X")[0]
    elif "&" in artist:
        actual_artist = artist.split("&")[0]
    elif "x" in artist.lower():
        actual_artist = artist.split("X")[0]
        actual_artist = artist.split("x")[0]
    else:
        actual_artist = artist'''
    actual_artist = artist.split("Featuring")[0]
    new_actual_artist = actual_artist.split("&")[0]
    final_artist = new_actual_artist.split("X")[0]

    
    '''try:
        new_artist = artist.split("Featuring")
        actual_artist = new_artist[0].strip()
    except:
        actual_artist = artist'''
    
    artist_name = final_artist.split()
    for x in artist_name:
        new_url += x
        new_url += "_"
    return new_url

def getartistLocation(url):
    try:
        new_url = url
        html = urlopen(new_url, context=ctx).read()
        soup = BeautifulSoup(html, "html.parser")
    
        location_reg = "[a-z|A-Z|\s]+,\s[a-z|A-Z|\s]+"
        tr_container = soup.find_all('tr')
        for tr in tr_container:
            th_container = tr.find_all('th')
            for th in th_container:
                if th.text == "Born":
                    reg_string = re.findall(location_reg, tr.text)
                elif th.text == "Origin":
                    first_reg_string = re.findall(location_reg, tr.text)
                    reg_string = []
                    for x in first_reg_string:
                        new_x = x.strip("Origin")
                        reg_string.append(new_x)
        final_location = reg_string[0]
        return(final_location)
    except:
        final_location = "Unknown"
        return(final_location)
        
def allArtistInfo(artists):
    artist_dict = {}
    unknown_count = []
    for artist in artists:
        x = getartistURL(artist)
        location = getartistLocation(x)
        artist_dict[artist] = location
    for x in artist_dict.keys():
        if artist_dict[x] == "Unknown":
            unknown_count.append(x)
    return artist_dict

def BillboardWriteToDatabase(artist_dict):
    cur.execute('DROP TABLE IF EXISTS Wikipedia')
    cur.execute('CREATE TABLE Wikipedia(source TEXT, artist TEXT, location TEXT)')
    source = "Billboard"
    for artist in artist_dict.keys():
        cur.execute("INSERT INTO Wikipedia (source, artist, location) VALUES (?,?,?)",(source, artist, artist_dict[artist]))
    conn.commit()

def SpotifyWriteToDatabase(artist_dict):
    source = "Spotify"
    for artist in artist_dict.keys():
        cur.execute("INSERT INTO Wikipedia (source, artist, location) VALUES (?,?,?)", (source, artist, artist_dict[artist]))
    conn.commit()



#cur.execute('CREATE TABLE Wikipedia(source TEXT, artist TEXT, song TEXT, location TEXT)')
billboard_artist_list = []
billboard_song_list = cur.execute("SELECT artist, song FROM Billboard")
for x in billboard_song_list:
    billboard_artist_list.append(x[0])
finalArtistInfo = allArtistInfo(billboard_artist_list)
BillboardWriteToDatabase(finalArtistInfo)
spotify_list = []
spotify_song_list = cur.execute("SELECT artist, song FROM Spotify")
for x in spotify_song_list:
    spotify_list.append(x[0])
spotifyArtistInfo = allArtistInfo(spotify_list)
SpotifyWriteToDatabase(spotifyArtistInfo)

#hi




