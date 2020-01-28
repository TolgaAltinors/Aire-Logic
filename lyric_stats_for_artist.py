import spotipy
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data

import requests
import urllib

import argparse
import sys
import string

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_track_names(sp_obj, artist, limit):
    '''
    search the spoitfy api for given artist and
    return a list of their songs

    Args:
        sp_obj (spotify object)    : to enable acceess
        artist id (string)         : artist name

    Returns:
        A set with track names
    '''

    spotify_tracks = set()

    # # Look for the artist's meta data - comes back as a dictionary
    search_result = sp_obj.search(q=artist, limit=limit)

    print ("Getting songs for '{0}'".format(artist))

    for track in search_result['tracks']['items']:

        track = track['name']

        # # strip some of the the text from the title name
        if "(" in track:
            track = track.split('(')[0]
        if "-" in track:
            track = track.split('-')[0]

        # # lower case and strip to avoid duplications
        track = track.strip().lower()

        # # Add to set
        spotify_tracks.add(track)

    return list(spotify_tracks)


def get_lyrics(artist, track):
    '''
    Get the lyrics from the API

    Args:
        artist (string)   : name of artist
        track (string)    : name of track

    Returns:
        The lyrics if found.
    '''

    base_url = 'https://api.lyrics.ovh/v1/'

    # # replace spaces with +
    artist = urllib.parse.quote_plus(artist)
    title = urllib.parse.quote_plus(track)

    # # Create full url
    url = base_url + artist + '/' + title

    response = ''
    lyrics = "** No lyrics **"

    found = '-- Not found --'
    message = "Lyrics for '{0}' -> {1}"
    
    try:
        # # read the url content
        response = urllib.request.urlopen(url).read()

        # # convert bytes to string
        lyrics = response.decode('utf-8')

        # # remove control characters
        lyrics = remove_control_characters(lyrics)
        
        found = '++ Found ++'
        print (message.format(track, found))

    except urllib.error.URLError as e: 
        print (message.format(track, found))
        print (e.reason)

    return lyrics  


def remove_control_characters(words):
    '''
    Remove control characters
    \n, \r, \t etc

    Args:
        words (string)    : contains lyrics
        
    Returns:
        The cleaned up lyrics.
    '''
    
    words = words.split(":")[1][:-1]

    words = words.replace('\\n', ' ')
    words = words.replace('\\r', ' ')
    words = words.replace('\\t', ' ')
    words = words.replace('\\', '')
    # # replace double spaces with one
    while words.find('  ') != -1:
        words = words.replace('  ', ' ')

    #words.strip(string.whitespace)
    return words


def produce_stats(tracks_df, artists):

    name_list = []   
    mean_list = []   
    max_list = []   
    min_list = []   
    std_dev_list = []
    var_list = []

    # # Loop throught the artists and check some statistics
    for artist in artists:

        # # remove any trailing spaces
        artist = artist.strip()

        name_list.append(artist)
        # # Filter out rows with matching artist
        true_flag =  tracks_df['Artist'] == artist
        df_matches = tracks_df[true_flag]       
   
        # # get the mean value of words
        mean_value = df_matches['Word_Count'].mean()
        mean_list.append(mean_value)
        print (f"The mean value for {artist}'s lyrics is {mean_value}")  

        # # get the max value of words
        max_value = df_matches['Word_Count'].max()
        max_list.append(max_value)
        print (f"The max value for {artist}'s lyrics is {max_value}")

        # # get the min value of words
        min_value = df_matches['Word_Count'].min()
        min_list.append(min_value)
        print (f"The min value for {artist}'s lyrics is {min_value}")

        # # create a pandas series
        pd_series = df_matches.Word_Count

        # # get the standard deviation value of words
        std_dev_value = pd_series.std()
        std_dev_list.append(std_dev_value)
        print (f"The standard deviation for {artist}'s lyrics is {std_dev_value}")

        # # get the variation value of words
        var_value = pd_series.var()
        var_list.append(var_value)
        print (f"The variation for {artist}'s lyrics is {var_value}")

        print (" ")



def main(argprser):

    client_id = '29a46e1c31b74e339f7f4dd1128b6314'
    client_secret = '3d27c8978264434e97f7c76b845980ed'
    
    # # parse artist details 
    artists = sys.argv[1].split(',')

    # # Create data frame to store track name and word counts
    tracks_df = pd.DataFrame(columns=['Artist', 'Track_Name', 'Word_Count'])

    # # Create a spotify object
    ccm = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp_obj = spotipy.Spotify(client_credentials_manager=ccm)

    # # Create a new artist list in case an artist was not found
    list_for_stats = []

    # # Loop through passed values
    for artist in artists:

        # # remove any trailing spaces
        artist = artist.strip()

        # # get tracks for the artist
        spotify_tracks = get_track_names(sp_obj, artist, 35)

        if len(spotify_tracks) > 0:
            
            # # Add artist to list where tracks were found
            list_for_stats.append(artist)

            for track in spotify_tracks:

                lyrics = get_lyrics(artist, track)

                if lyrics != '** No lyrics **':
                    
                    # # word count
                    word_count = len(lyrics.split(' ')) + 1

                    tracks_df.loc[len(tracks_df)] = [artist, track, word_count]
        else:
            print ("*******************")
            print ("No tracks for {0} found".format(artist))    
            print ("*******************")

        print (" ")
        print (" ")


    # # Produce some stats
    produce_stats(tracks_df, list_for_stats)
   

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("Artist", type=str)
    argparser = parser.parse_args()

    main(argparser)

    # # example run
    #python lyric_stats_for_artist.py "Linkin Park"     --> Should produce stats on console
    #python lyric_stats_for_artist.py "Linkin Park,Stormzy,Adele,Sam Smith" --> Should produce stats on console and pop up graphs 
    #python lyric_stats_for_artist.py "Linkin Park,Stormzy,Adele,ZlaXlah" --> Should produce stats on console and pop up graphs (minus ZlaXlah as it does not exist)
    
