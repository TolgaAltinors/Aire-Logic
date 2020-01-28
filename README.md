# Aire-Logic
Test on API's

The script is written in Python 3 and it is a command line application.

It accepts 1 argument in the shape of a string.

It can be a single artist "Stormzy" or a list of artists like "Stormzy,Linkin Park,Adele".

It utilises the Spotify API to retrieve songs per artists. 
I have included a limit in the script for the number of songs to be returned. This is part of the 
"get_track_names" function call.

-----------------------------------------------------------------------------------------
Libraries
-----------------------------------------------------------------------------------------
The following python libraries need to be present for the script to execute successfully. 
Numpy should be installed as part of pandas.

1 - spotipy     (pip install spotipy)
2 - pandas      (pip install pandas)
3 - numpy       (pip install numpy)
4 - requests    (pip install requests)
5 - matplotlib  (pip install matplotlib)

-----------------------------------------------------------------------------------------
Running of the script
-----------------------------------------------------------------------------------------
Below are examples of how the script can be run.

python lyric_stats_for_artist.py "Linkin Park"
  --> (Should produce stats on console)

python lyric_stats_for_artist.py "Linkin Park,Stormzy,Adele,Sam Smith"
  --> (Should produce stats on console and pop up graphs)

python lyric_stats_for_artist.py "Linkin Park,Stormzy,Adele,ZlaXlah"
  --> (Should produce stats on console and pop up graphs, minus ZlaXlah as it does not exist)

