#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 20:21:14 2021

@author: ericaschultz
"""

#Notebook for Spotify data

#Importing packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json


#Playlist Dataframe
##########################################################################################

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
        play_df.dropna(subset = ['trackName'],inplace = True)
    #If it's not the first iteration then we append to play_df
    else:
        temp['lastModifiedDate'] = playlists['lastModifiedDate'].iloc[i]
        temp['description'] = playlists['description'].iloc[i]
        temp['numberOfFollowers'] = playlists['numberOfFollowers'].iloc[i]
        play_df = play_df.append(temp)
        
    #To show the progress of the loop because I'm anxious 
    print(i)

play_df.reset_index(inplace = True, drop = True)
    
#To check that there are 81 playlists:
assert len(play_df.playlist_name.unique()) == 81



#Streaming History
##########################################################################################

with open("/Users/ericaschultz/Desktop/My_Projects/DATA/spotify/MyData/StreamingHistory0.json") as file:
    data1 = json.load(file)
    
stream_df = pd.DataFrame.from_dict(data1)


file_names = ['StreamingHistory1', 'StreamingHistory2', 'StreamingHistory3']
path = '/Users/ericaschultz/Desktop/My_Projects/DATA/spotify/MyData/'
file_names = [path + i + '.json' for i in file_names]

for i in file_names:
    with open(i) as file:
        temp = json.load(file)
    temp_df = pd.DataFrame.from_dict(temp)
    stream_df = pd.concat([stream_df, temp_df], ignore_index=True)
    
    
#What are the total msPlayed for each song?
stream_df.groupby('trackName').msPlayed.sum().sort_values()
#There is an issue here because podcasts are counting as a track. I'm trying to think of the best way to figure out which tracks are podcasts.

tracks_notin_library = list(set(stream_df.artistName) - set(play_df.artistName))

oddsongs_total_msPlayed = stream_df.loc[stream_df.artistName.isin(tracks_notin_library)].groupby('trackName').msPlayed.sum().sort_values(ascending = False)
oddsongs_df = pd.DataFrame(oddsongs_total_msPlayed)

oddsongs_df = stream_df[['artistName', 'trackName']].merge(oddsongs_df, how = 'right', on = 'trackName')
oddsongs_df.drop_duplicates(inplace = True)

podcast_names = ['The Joe Rogan Experience', 'The Daily', 'Build a Career in Data Science', 'Mike and Brooker Show', 'Chicks in the Office']
stream_df = stream_df[~stream_df.artistName.isin(podcast_names)]
#now let's try again
stream_df.groupby('trackName').msPlayed.sum().sort_values(ascending = False)
