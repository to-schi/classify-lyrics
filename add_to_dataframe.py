"""
Command line tool to add scraped lyrics to a dataframe
"""
import argparse
import os
import pathlib

import pandas as pd

from utils.farben import Color

parser = argparse.ArgumentParser(
    description="This program adds lyrics of 1 ARTIST to a DataFrame-csv"
)
parser.add_argument("artist", help="ARTIST-name", type=str)
parser.add_argument("folder", help="FOLDER with lyrics-files", type=str, nargs="?")
args = parser.parse_args()
ARTIST = args.artist
FOLDER = args.folder

if FOLDER is None:
    FOLDER = "./" + ARTIST + "_lyrics"


def combine_lyrics(artist, folder):
    """
    Adds content of all txt-files in named FOLDER to lyrics_dataframe.csv.
    """
    if os.path.isfile("./lyrics_dataframe.csv") is True:
        print(
            Color.cyan
            + "lyrics_dataframe.csv"
            + Color.green
            + " found\n"
            + Color.end
            + "Adding lyrics of "
            + Color.yellow
            + artist
            + Color.end
        )
        lyrics_dataframe = pd.read_csv(
            "./lyrics_dataframe.csv", index_col=[0], encoding="utf-8"
        )
        current_set = []
        for file in pathlib.Path(folder).iterdir():
            if file.is_file():
                current_song = []
                current_file = open(file, "r", encoding="utf-8")
                for line in current_file:
                    current_song.append(line + " ")
                current_song = "".join(current_song)
                current_set.append(current_song)
                current_file.close()
        current_set = pd.DataFrame(current_set, columns=["songs"])
        current_set["labels"] = artist
        lyrics_dataframe = pd.concat([lyrics_dataframe, current_set])
        lyrics_dataframe.reset_index(drop=True, inplace=True)
        lyrics_dataframe.to_csv("./lyrics_dataframe.csv")
        print(
            "All lyrics in "
            + Color.cyan
            + FOLDER
            + Color.end
            + " have been added to "
            + Color.cyan
            + "lyrics_dataframe.csv"
            + Color.end
        )
    else:
        print(
            Color.cyan
            + "lyrics_dataframe.csv"
            + Color.end
            + Color.red
            + " not found\n"
            + Color.end
            + "Creating new Dataframe with lyrics of "
            + Color.yellow
            + artist
            + Color.end
        )
        current_set = []
        for file in pathlib.Path(folder).iterdir():
            if file.is_file():
                current_song = []
                current_file = open(file, "r", encoding="utf-8")
                for line in current_file:
                    current_song.append(line + " ")
                current_song = "".join(current_song)
                current_set.append(current_song)
                current_file.close()
        current_set = pd.DataFrame(current_set, columns=["songs"])
        current_set["labels"] = artist
        current_set.to_csv("./lyrics_dataframe.csv", encoding="utf-8")
        print(
            "All lyrics in "
            + Color.cyan
            + FOLDER
            + Color.end
            + " have been added to "
            + Color.cyan
            + "lyrics_dataframe.csv"
            + Color.end
        )


combine_lyrics(ARTIST, FOLDER)
