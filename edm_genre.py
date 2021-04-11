import pandas as pd
import numpy as np

#import genre data
genre_df = pd.read_csv('spotify_artist_genres.csv')

#function to check if genre is edm
def is_edm(genre_array):
    #lowercase/strip
    for item in genre_array:
        item = item.lower()
        item = item.strip()

    #list of edm genres
    genres_list = ['edm', 'breakbeat', 'chiptune', 'downtempo', 'drumandbass','dub',
     'electro','hardstyle','idm','synth-pop','house','techno','trance', 'ukbass', 'wonky']

    #save rows with edm genres, delete others#
    check = any(item in genre_array for item in genres_list)
    if(check):
        return genre_array
    else:
        return None

#exract edm genre data from dataframe
edm_df = genre_df
edm_df['genres'] = edm_df['genres'].apply(is_edm)
edm_df = edm_df.dropna()

#artist array
artist_column = edm_df.loc[:,'name']
artist_array = artist_column.values


#sort spotify data with edm results
spotify_df = pd.read_csv('spotify_results.csv')

def artist_match(artist):
    if(artist in artist_array):
        return artist
    else:
        return None

spotify_df['name'] = spotify_df['name'].apply(artist_match)
spotify_df = spotify_df.dropna()
print(len(spotify_df.index))
##print(spotify_df.columns)
