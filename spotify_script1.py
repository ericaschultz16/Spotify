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


test = pd.DataFrame(playlists['items'].iloc[0])
test = pd.concat([test.drop(['track'], axis = 1), test['track'].apply(pd.Series)], axis = 1)

