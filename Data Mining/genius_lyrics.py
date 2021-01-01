import lyricsgenius
import pandas as pd
import numpy as np
import time

from requests.exceptions import ConnectionError


def read_xlsx(file_name):
    """
    Read data set xlsx file.

    Note: other columns can be mined in the same way as below.
    """

    # Collect column data in pd data frames
    song_names  = pd.read_excel(file_name, skiprows=0, usecols=[1])
    albums      = pd.read_excel(file_name, skiprows=0, usecols=[2])
    artists     = pd.read_excel(file_name, skiprows=0, usecols=[3])
    years       = pd.read_excel(file_name, skiprows=0, usecols=[4])
    classes     = pd.read_excel(file_name, skiprows=0, usecols=[17])

    # Convert pd data frames to lists
    song_names  = song_names.values.tolist()
    albums      = albums.values.tolist()
    artists     = artists.values.tolist()
    years       = years.values.tolist()
    classes     = classes.values.tolist()

    # Flatten lists
    song_names  = [item for sublist in song_names for item in sublist]
    albums      = [item for sublist in albums for item in sublist]
    artists     = [item for sublist in artists for item in sublist]
    years       = [item for sublist in years for item in sublist]
    classes     = [item for sublist in classes for item in sublist]

    # Convert to array for easier access
    song_names  = np.asarray(song_names)
    albums      = np.asarray(albums)
    artists     = np.asarray(artists)
    years       = np.asarray(years)
    classes     = np.asarray(classes)

    return song_names, albums, artists, years, classes


def collect_lyrics(song_names, artists, albums, years, classes):
    """
    Function to get lyrics for each song / artist pair.
    """

    # Genius API connection through access token
    genius = lyricsgenius.Genius("9okpMM_KZMCChUiFRhI-s_vCgXHwYsCAqN7T-SIjz5E7i_mI-G7_KWw0GwS6Qr7D")

    # Go through all songs and get lyrics
    lyrics_found        = []
    lyrics_not_found    = []
    garbage             = []

    for x in range(len(song_names)):
        print(x)

        try:
            song = genius.search_song(song_names[x], artists[x])

            # Garbage is for songs that return wrong data (easy to spot due to length)
            if (len(song.lyrics) > 10000):
                garbage.append([song_names[x], artists[x], albums[x], years[x], song.lyrics, classes[x]])
                print("Garbage!!!")

            else:
                lyrics_found.append([song_names[x], artists[x], albums[x], years[x], song.lyrics, classes[x]])

        except Exception as e:
            print("Lyrics not found!")
            lyrics_not_found.append([song_names[x], artists[x], albums[x], years[x], classes[x]])

    # Return both lyrics found and not found for later processing
    return lyrics_found, lyrics_not_found, garbage


def main():
    song_names, albums, artists, years, classes = read_xlsx("clean_spotify.xlsx")   
    lyrics_found, lyrics_not_found, garbage = collect_lyrics(song_names, artists, albums, years, classes)

    # Create CSV file for lyrics found and not found
    df1 = pd.DataFrame(lyrics_found, columns = ['Name', 'Artist', 'Album', 'Release Date', 'Lyrics', 'Class'])
    df1.to_csv("lyrics_found.csv", sep = ',')

    df2 = pd.DataFrame(garbage, columns = ['Name', 'Artist', 'Album', 'Release Date', 'Lyrics', 'Class'])
    df2.to_csv("garbage.csv", sep = ',')

    df3 = pd.DataFrame(lyrics_not_found, columns = ['Name', 'Artist', 'Album', 'Release Date', 'Class'])
    df3.to_csv("lyrics_not_found.csv", sep = ',')


main()