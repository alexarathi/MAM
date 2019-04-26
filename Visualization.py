import matplotlib
import matplotlib.pyplot as plt 
import sqlite3
import json
import unittest

#established connection with Database
conn = sqlite3.connect('SIProject.sqlite')
cur = conn.cursor()

#creating dictionary for calculations file
all_data = {}

def get_spotify_dict(siprojectdb):
    
    #initializes the variables
    spotify_dict = {}
    mam_song_count = 0
    party_song_count = 0
    si206_song_count = 0

    #grabs song from each row in Billboard Table/Separates from Tuple/Adds all songs to a list
    cur.execute('SELECT song FROM Billboard')
    billboard_list = []
    for x in cur:
        billboard_list.append(x[0])

    #Grabs songs from the MAM JAMS! Playlist(stored in mam_playlist) and checks if it is in the Billboard Top 100. Adds resulting count to dictionary
    mam_playlist = cur.execute('SELECT playlist_name, song, artist FROM Spotify WHERE playlist_name = "MAM JAMS! "')
    for row in mam_playlist:
        if row[1] in billboard_list:
            mam_song_count += 1
    spotify_dict['MAM JAMS! '] = mam_song_count

    #Grabs songs from the Party! Playlist(stored in party_playlist) and checks if each song is in the Billboard Top 100. Adds resulting count to dictionary
    party_playlist = cur.execute('SELECT playlist_name, song, artist FROM Spotify WHERE playlist_name = "Party!"')
    for row in party_playlist:
        if row[1] in billboard_list:
            party_song_count += 1
    spotify_dict['Party!'] = party_song_count

    #Grabs songs from the SI 206! Playlist(stored in si206_playlist) and checks if each song is in the Billboard Top 100. Adds resulting count to the dictionary
    si206_playlist = cur.execute('SELECT playlist_name, song, artist FROM Spotify WHERE playlist_name = "SI 206!"')
    for row in si206_playlist:
        if row[1] in billboard_list:
            si206_song_count += 1
    spotify_dict['SI 206!'] = si206_song_count

    #Adds the dictionary of playlists and counts in top 100 to the total calculations dictionary
    all_data['Spotify Playlist Billboard Count'] = spotify_dict
    return(spotify_dict)

def spotify_billboard_visualization(spotify_dict):
    
    #sets lists that will be used for x and y values
    names = spotify_dict.keys()
    vals = spotify_dict.values()
    
    #creates graph
    fig, ax = plt.subplots()
    
    #gives value for graph and sets color of each bar
    plt.bar(names, vals, color = ['red', 'blue', 'cyan'])

    #sets more information for graph axis
    ax.set_xlabel("Playlist Name")
    ax.set_ylabel("# of Songs in Top 100")
    ax.set_title("Songs per Playlist in Top 100")

    #presents the graph
    plt.show()

def get_billboard_artist_location(siprojectdb):
    
    #initializes the dictionary (key = location, value = how many artists are from there)
    location_dict = {}
    
    #grabs tuple list of artists from Billboard Table/Adds them to a list of just artists
    cur.execute('SELECT artist FROM Billboard')
    billboard_list = []
    for row in cur:
        billboard_list.append(row[0])
    
    #Grabs tuple list of Billboard artists and their locations
    wikipedia_info = cur.execute('SELECT source, artist, location FROM Wikipedia WHERE source = "Billboard"')

    #Loops through each wikipedia group/Checks if the artist is in the list of artists from Billboard/Updates count for each location in location_dict
    for artist in wikipedia_info:
        if artist[1] in billboard_list:
            if artist[2] in location_dict.keys():
                location_dict[artist[2]] += 1
            else:
                location_dict[artist[2]] = 1
    #Adds the location dictionary to the final calculations dictionary
    all_data['Billboard Artist Locations'] = location_dict
    return(location_dict)

def billboard_location_visualization(location_dict):
    #sets list that will be used for x and y values of the graph
    names = location_dict.keys()
    vals = location_dict.values()
    
    #creates the graph
    fig, ax = plt.subplots()

    #extends the x values apart
    fig.subplots_adjust(bottom = 0.3)

    #changes the font size of each x value
    for tick in ax.xaxis.get_major_ticks(): 
        tick.label.set_fontsize(4)
    #sets the values of the graph
    plt.bar(names, vals, color = ['blue', 'green', 'red', 'cyan', 'purple', 'black', 'magenta', 'yellow', 'lightblue', 'orange'])
    #makes x values vertical instead of horizontal
    plt.xticks(rotation = 90)
    
    #sets the axis labels and title for graph
    ax.set_xlabel("Playlist Name")
    ax.set_ylabel("# of Songs in Top 100")
    ax.set_title("Songs per Playlist in Top 100")

    #presents the graph
    plt.show()

def get_spotify_location_dict(siprojectdb):
    #initializes dictionary holding (key = each playlist | value = dictionary of each playlist (key = location | value = count of artists from that location))
    spotify_location_dict = {}

    #grabs artists from Spotify Table with MAM JAMS! as playlist and adds to a list
    mam_dict = {}
    cur.execute('SELECT playlist_name, artist FROM Spotify WHERE playlist_name = "MAM JAMS! "')
    mam_playlist = []
    for row in cur:
        mam_playlist.append(row[1])
    
    #grabs artists from Spotify Table with Party! as playlist and adds to a list
    party_dict = {}
    cur.execute('SELECT playlist_name, artist FROM Spotify WHERE playlist_name = "Party!"')
    party_playlist = []
    for row in cur:
        party_playlist.append(row[1])

    #grabs artists from Spotify Table with SI 206! as playlist and adds to a list
    si_dict = {}
    cur.execute('SELECT playlist_name, artist FROM Spotify WHERE playlist_name = "SI 206!"')
    si_playlist = []
    for row in cur:
        si_playlist.append(row[1])

    #Grabs all info from Wikipedia Table with Spotify as source
    wikipedia_info = cur.execute('SELECT source, artist, location FROM Wikipedia WHERE source = "Spotify"')
    #Loops through wikipedia items/Checks if artist is in each playlist/Updates each playlist dictionary for location and count of artists there
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
    #Adds each playlist dictionary to the total spotify location dictionary
    spotify_location_dict['MAM JAMS!'] = mam_dict
    spotify_location_dict['Party!'] = party_dict
    spotify_location_dict['SI 206!'] = si_dict

    #Adds spotify location calculations to calculations dictionary
    all_data['Spotify Artist Locations'] = spotify_location_dict
    return(spotify_location_dict)




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

#Runs Spotify and Billboard Info/Visualization
spotify_billboard_dict = get_spotify_dict('SIProject.sqlite')
spotify_billboard_visualization(spotify_billboard_dict)

#Runs Billboard and Wikipedia Location Info/Visualization
location_dict = get_billboard_artist_location('SIProject.sqlite')
billboard_location_visualization(location_dict)

#Runs Spotify and Wikipedia Location Info/Visualization
spotify_info_dict = get_spotify_location_dict('SIProject.sqlite')
spotify_location_visualization(spotify_info_dict)

#Creates JSON file for calculations
filename = open('SIProject.json', 'w')
filename.write(json.dumps(all_data))
filename.close()