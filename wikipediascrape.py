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

#establishes connection with SIProject Database
conn = sqlite3.connect('SIProject.sqlite')
cur = conn.cursor()

def getartistURL(artist):
    
    new_url = "https://en.wikipedia.org/wiki/"
    
    #Sets the artist as the main artist listed, no features
    actual_artist = artist.split("Featuring")[0]
    new_actual_artist = actual_artist.split("&")[0]
    final_artist = new_actual_artist.split("X")[0]
    
    #creates url based on typical wikipedia format, splitting up artist name with underscores substituting spaces
    artist_name = final_artist.split()
    for x in artist_name:
        new_url += x
        new_url += "_"
    return new_url

def getartistLocation(url):
    #set try except statement where it would look for birthplace, if it couldn't be found "unknown"
    try:
        new_url = url
        html = urlopen(new_url, context=ctx).read()
        soup = BeautifulSoup(html, "html.parser")
        #sets the regex statement to search for a location
        location_reg = "[a-z|A-Z|\s]+,\s[a-z|A-Z|\s]+"
        #finds a list of all tr tags
        tr_container = soup.find_all('tr')
        for tr in tr_container:
            #finds a list of all th tags in each tr
            th_container = tr.find_all('th')
            for th in th_container:
                #searches for "Born" or "Origin" and if found, returns the regex of the tr tag it is in
                if th.text == "Born":
                    reg_string = re.findall(location_reg, tr.text)
                elif th.text == "Origin":
                    first_reg_string = re.findall(location_reg, tr.text)
                    reg_string = []
                    #Origin returned a weird regex with Origin attached to the front, so we stripped that
                    for x in first_reg_string:
                        new_x = x.strip("Origin")
                        reg_string.append(new_x)
        final_location = reg_string[0]
        return(final_location)
    except:
        #if regex could not be found, the failsafe was the except statement
        final_location = "Unknown"
        return(final_location)
        
def allArtistInfo(artists):
    artist_dict = {}
    unknown_count = []
    #loops through artist list and applies the above functions. Stores them in a dictionary with the artist as key and location as value
    for artist in artists:
        x = getartistURL(artist)
        location = getartistLocation(x)
        artist_dict[artist] = location
    for x in artist_dict.keys():
        if artist_dict[x] == "Unknown":
            unknown_count.append(x)
    return artist_dict

def BillboardWriteToDatabase(artist_dict):
    #creates the Wikipedia Table and for each artist, inserts their data into the Table
    cur.execute('DROP TABLE IF EXISTS Wikipedia')
    cur.execute('CREATE TABLE Wikipedia(source TEXT, artist TEXT, location TEXT)')
    source = "Billboard"
    for artist in artist_dict.keys():
        cur.execute("INSERT INTO Wikipedia (source, artist, location) VALUES (?,?,?)",(source, artist, artist_dict[artist]))
    conn.commit()

def SpotifyWriteToDatabase(artist_dict):
    #For each artist from spotify, inserts their data into the Table
    source = "Spotify"
    for artist in artist_dict.keys():
        cur.execute("INSERT INTO Wikipedia (source, artist, location) VALUES (?,?,?)", (source, artist, artist_dict[artist]))
    conn.commit()

#Creates a list of artists from Billboard
billboard_artist_list = []
billboard_song_list = cur.execute("SELECT artist, song FROM Billboard")
for x in billboard_song_list:
    billboard_artist_list.append(x[0])
#Gets their info in the dictionary and writes it to the Wikipedia Table
finalArtistInfo = allArtistInfo(billboard_artist_list)
BillboardWriteToDatabase(finalArtistInfo)

#Creates a list of artists from Spotify
spotify_list = []
spotify_song_list = cur.execute("SELECT artist, song FROM Spotify")
for x in spotify_song_list:
    spotify_list.append(x[0])
#Gets their info in the dictionary and writes it to the Wikipedia Table
spotifyArtistInfo = allArtistInfo(spotify_list)
SpotifyWriteToDatabase(spotifyArtistInfo)




