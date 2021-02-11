#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 20:21:14 2021

@author: ericaschultz
"""

#Notebook for Spotify data

#importing packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json

with open("/Users/ericaschultz/Desktop/My_Projects/DATA/spotify/MyData/YourLibrary.json") as file:
    data = json.load(file)
    
df_keys = data.keys()    
tracks = pd.DataFrame.from_dict(data['tracks'])
albums = pd.DataFrame.from_dict(data['albums'])
bannedTracks = pd.DataFrame.from_dict(data['bannedTracks'])
other = pd.DataFrame.from_dict(data['other'])



with open("/Users/ericaschultz/Desktop/My_Projects/DATA/spotify/MyData/StreamingHistory0.json") as file:
    data1 = json.load(file)
    
stream0 = pd.DataFrame.from_dict(data1)

tracks_stream = pd.merge(tracks, stream0, left_on = "track", right_on = "trackName", how = 'right')


with open("/Users/ericaschultz/Desktop/My_Projects/DATA/spotify/MyData/Playlist1.json") as file:
    data2 = json.load(file)   
playlists = pd.DataFrame.from_dict(data2['playlists'])

play_df = playlists.copy()

for i in playlists.index:
    #Create new df from items object in row i. This only has one column with each column being a dictionary for a specific song
    temp = pd.DataFrame(playlists['items'].iloc[i])
    
    if temp.empty:
        temp['playlist_name'] = playlists['name'].iloc[i]
        temp['lastModifiedDate'] = playlists['lastModifiedDate'].iloc[i]
        temp['description'] = playlists['description'].iloc[i]
        temp['numberOfFollowers'] = playlists['numberOfFollowers'].iloc[i]
        temp['episode'] = None
        temp['localTrack'] = None
        temp['trackName'] = None
        temp['artistName'] = None
        temp['albumName'] = None
        play_df = play_df.append(temp)
        continue
    
    #We take the dictionary and convert it to a series we can concatonate to the df itself.
    #This effectively takes the keys of the song dictionary and makes them into columns with their respective values
    temp = pd.concat([temp.drop(['track'], axis = 1), temp['track'].apply(pd.Series)], axis = 1)
    
    #Make a column specifying the playlist name using the location in the playlists df
    temp['playlist_name'] = playlists['name'].iloc[i]
    
    
    #If this is the first iteration, then we create the dataframe with the appropriate columns
    if i == 0:
        play_df = pd.merge(play_df, temp, how = 'outer', left_on = 'name', right_on = 'playlist_name')
        play_df = play_df.drop(["name",'items'], axis = 1)
    #If it's not the first iteration then we append to play_df
    else:
        temp['lastModifiedDate'] = playlists['lastModifiedDate'].iloc[i]
        temp['description'] = playlists['description'].iloc[i]
        temp['numberOfFollowers'] = playlists['numberOfFollowers'].iloc[i]
        play_df = play_df.append(temp)
        
    #To show the progress of the loop because I'm anxious 
    print(i)
    
#To check that there are 82 playlists:
#len(play_df.playlist_name.unique()


#





