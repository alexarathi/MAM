import matplotlib
import matplotlib.pyplot as plt 
import sqlite3
import json
import unittest

conn = sqlite3.connect('SIProject.sqlite')
cur = conn.cursor()

def get_spotify_dict(siprojectdb):
    spotify_dict = {}
    mam_song_count = 0
    party_song_count = 0
    si206_song_count = 0

    cur.execute('SELECT song FROM Billboard')
    billboard_list = []
    for x in cur:
        billboard_list.append(x[0])

    mam_playlist = cur.execute('SELECT playlist_name, song, artist FROM Spotify WHERE playlist_name = "MAM JAMS! "')
    for row in mam_playlist:
        if row[1] in billboard_list:
            mam_song_count += 1
    spotify_dict['MAM JAMS! '] = mam_song_count

    party_playlist = cur.execute('SELECT playlist_name, song, artist FROM Spotify WHERE playlist_name = "Party!"')
    for row in party_playlist:
        if row[1] in billboard_list:
            party_song_count += 1
    spotify_dict['Party!'] = party_song_count

    si206_playlist = cur.execute('SELECT playlist_name, song, artist FROM Spotify WHERE playlist_name = "SI 206!"')
    for row in si206_playlist:
        if row[1] in billboard_list:
            si206_song_count += 1
    spotify_dict['SI 206!'] = si206_song_count
    return(spotify_dict)

def spotify_billboard_visualization(spotify_dict):
    names = spotify_dict.keys()
    vals = spotify_dict.values()
    
    fig, ax = plt.subplots()
    
    plt.bar(names, vals, color = ['red', 'blue', 'cyan'])

    ax.set_xlabel("Playlist Name")
    ax.set_ylabel("# of Songs in Top 100")
    ax.set_title("Songs per Playlist in Top 100")
    plt.show()

def get_billboard_artist_location(siprojectdb):
    location_dict = {}
    
    cur.execute('SELECT artist FROM Billboard')
    billboard_list = []
    for row in cur:
        billboard_list.append(row[0])
    
    wikipedia_info = cur.execute('SELECT source, artist, location FROM Wikipedia WHERE source = "Billboard"')
    for artist in wikipedia_info:
        if artist[1] in billboard_list:
            if artist[2] in location_dict.keys():
                location_dict[artist[2]] += 1
            else:
                location_dict[artist[2]] = 1
    return(location_dict)

def billboard_location_visualization(location_dict):
    names = location_dict.keys()
    print(len(names))
    vals = location_dict.values()
    
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom = 0.3)
    for tick in ax.xaxis.get_major_ticks(): 
        tick.label.set_fontsize(4)
    plt.bar(names, vals, color = ['blue', 'green', 'red', 'cyan', 'purple', 'black', 'magenta', 'yellow', 'lightblue', 'orange'])
    plt.xticks(rotation = 90)
    

    ax.set_xlabel("Playlist Name")
    ax.set_ylabel("# of Songs in Top 100")
    ax.set_title("Songs per Playlist in Top 100")
    plt.show()

def get_spotify_location_dict(siprojectdb):
    spotify_dict = {}

    mam_dict = {}
    cur.execute('SELECT playlist_name, artist FROM Spotify WHERE playlist_name = "MAM JAMS! "')
    mam_playlist = []
    for row in cur:
        mam_playlist.append(row[1])
    
    party_dict = {}
    cur.execute('SELECT playlist_name, artist FROM Spotify WHERE playlist_name = "Party!"')
    party_playlist = []
    for row in cur:
        party_playlist.append(row[1])

    si_dict = {}
    cur.execute('SELECT playlist_name, artist FROM Spotify WHERE playlist_name = "SI 206!"')
    si_playlist = []
    for row in cur:
        si_playlist.append(row[1])

    wikipedia_info = cur.execute('SELECT source, artist, location FROM Wikipedia WHERE source = "Spotify"')
    for row in wikipedia_info:
        if row[1] in mam_playlist:
            if row[2] in mam_dict.keys():
                mam_dict[row[2]] += 1
            else:
                mam_dict[row[2]] = 1
        if row[1] in party_playlist:
            if row[2] in party_dict.keys():
                party_dict[row[2]] += 1
            else:
                party_dict[row[2]] = 1
        if row[1] in si_playlist:
            if row[2] in si_dict.keys():
                si_dict[row[2]] += 1
            else:
                si_dict[row[2]] = 1
    spotify_dict['MAM JAMS!'] = mam_dict
    spotify_dict['Party!'] = party_dict
    spotify_dict['SI 206!'] = si_dict
    return(spotify_dict)




def spotify_location_visualization(spotify_location_dict):
   

    names = spotify_location_dict['MAM JAMS!'].keys()
    names2 = spotify_location_dict['Party!'].keys()
    names3 = spotify_location_dict['SI 206!'].keys()

    values = spotify_location_dict['MAM JAMS!'].values()
    values2 = spotify_location_dict['Party!'].values()
    values3 = spotify_location_dict['SI 206!'].values()

    fig = plt.figure(figsize = (10,25))

    ax1 = fig.add_subplot(421)
    ax1.set_title("MAM JAMS!")
    ax1.set_xlabel("Locations")
    ax1.set_ylabel("# of Songs")
    fig.subplots_adjust(bottom = 0.3)

    for tick in ax1.xaxis.get_major_ticks(): 
        tick.label.set_fontsize(4)
    plt.bar(names, values, color = ['blue', 'green', 'red', 'cyan', 'purple', 'black', 'magenta', 'yellow', 'lightblue', 'orange'])
    plt.xticks(rotation = 90)

    ax2 = fig.add_subplot(422)
    ax2.set_title("Party!")
    ax2.set_xlabel("Locations")
    ax2.set_ylabel("# of Songs")
    fig.subplots_adjust(bottom = 0.3)

    for tick in ax2.xaxis.get_major_ticks(): 
        tick.label.set_fontsize(4)
    plt.bar(names2, values2, color = ['blue', 'green', 'red', 'cyan', 'purple', 'black', 'magenta', 'yellow', 'lightblue', 'orange'])
    plt.xticks(rotation = 90)

    ax3 = fig.add_subplot(542)
    ax3.set_title("SI 206!")
    ax3.set_xlabel("Locations")
    ax3.set_ylabel("# of Songs")
    fig.subplots_adjust(bottom = 0.3)

    for tick in ax3.xaxis.get_major_ticks(): 
        tick.label.set_fontsize(4)
    plt.bar(names3, values3, color = ['blue', 'green', 'red', 'cyan', 'purple', 'black', 'magenta', 'yellow', 'lightblue', 'orange'])
    plt.xticks(rotation = 90)

    plt.show()


'''spotify_billboard_dict = get_spotify_dict('SIProject.sqlite')
spotify_billboard_visualization(spotify_billboard_dict)'''
'''location_dict = get_billboard_artist_location('SIProject.sqlite')
billboard_location_visualization(location_dict)'''
spotify_info_dict = get_spotify_location_dict('SIProject.sqlite')
spotify_location_visualization(spotify_info_dict)