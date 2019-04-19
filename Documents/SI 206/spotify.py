
import spotify_info
import requests
import json
import sqlite3
import webbrowser

import urllib.request, urllib.parse, urllib.error
import sys
import os
import spotipy 
import spotipy.util as util
import matplotlib
import matplotlib.pyplot as plt 


clientid = spotify_info.consumer_key
clientid_secret = spotify_info.secret_key
redirecturi = spotify_info.redirect_uri

#get the username from terminal
username = 'miriam_akkary@yahoo.com'
scope = 'user-library-read'
try: 
    token = util.prompt_for_user_token(username, scope,client_id=clientid, client_secret= clientid_secret, redirect_uri= redirecturi)

except: 
    os.remove(f'.cache-{username}')
    token = util.prompt_for_user_token(username, scope,client_id=clientid, client_secret= clientid_secret, redirect_uri= redirecturi)



#token = util.prompt_for_user_token(username, scope,client_id=clientid, client_secret= clientid_secret, redirect_uri= redirecturi)
#creating spotify object
spotify_object = spotipy.Spotify(auth=token)

#gets content from the current spotify user
user = spotify_object.current_user()
#print(json.dumps(user, sort_keys=True, indent=4))

#gets current users playlists
results = spotify_object.current_user_playlists()
#creates a list of playlist ID numbers
playlist_list = []
for x in results['items']:
    playlist_name = x["id"]
    playlist_list.append(playlist_name)
print(playlist_list)

# makes a dictionary where the key is the ID number and the value are all the songs in the playlist
playlist_result_dict = {}
playlist_count = 0
for x in playlist_list:
    playlist_result_dict[x] = spotify_object.user_playlist(username, playlist_id = x)
    #new_results = spotify_object.user_playlist(username, x)

#gets all the individua songs in the playlist and adds them to a dictionary 
songs_in_playlist = {}
for playlist_id in playlist_result_dict.keys():
    song_list = []
    for y in playlist_result_dict[playlist_id]["tracks"]['items']:
        song_name = y['track']['name']
        song_list.append(song_name)
    songs_in_playlist[playlist_id] = song_list

print(songs_in_playlist)


try:
    filename = open('spotify.json', 'r')
    file_results = json.loads(filename)
    filename.close()
    filename = open('spotify.json', 'w')
    for x in playlist_result_dict.keys():
        if x not in file_result.keys():
            filename.write(json.dumps(playlist_result_dict[x]))

except:
    filename = open('spotify.json', 'w')
    filename.write(json.dumps(playlist_result_dict))












