import numpy as np
import pandas as pd
import lyricsgenius

"""
Script for mining a few extra songs for data set.
"""

def main():

    genius = lyricsgenius.Genius("9okpMM_KZMCChUiFRhI-s_vCgXHwYsCAqN7T-SIjz5E7i_mI-G7_KWw0GwS6Qr7D")

    artist = genius.search_artist("Frank Sinatra", max_songs=715, sort="title", include_features=True)

    lyrics_found = []

    #print(artist.songs)

    for el in artist.songs:
        try:
            temp = str(el)
            temp = temp.split("by",1)[0]
            temp = temp.replace("\"", "")
            print(temp)
            lyrics_found.append([temp, "Frank Sinatra", el.album, "N/A", el.lyrics, "Jazz"])

        except Exception as e:
            print("Exception thrown!")
            print(e)


    df = pd.DataFrame(lyrics_found, columns = ['Name', 'Artist', 'Album', 'Release Date', 'Lyrics', 'Class'])
    df.to_csv("andrea_bocelli.csv", sep = ',')


main()