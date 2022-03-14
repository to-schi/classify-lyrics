from utils.farben import color
import pandas as pd
import os
import pathlib
import argparse

parser = argparse.ArgumentParser(
    description="This program adds lyrics of 1 artist to a DataFrame-csv")
parser.add_argument("artist", help="artist-name", type=str)
parser.add_argument("folder", help="folder with lyrics-files",
                    type=str, nargs='?')
args = parser.parse_args()
artist = args.artist
folder = args.folder

if folder == None: folder = "./"+artist+"_lyrics"

def combine_lyrics(artist, folder):
    '''
    Adds content of all txt-files in named folder to lyrics_dataframe.csv.
    '''
    if os.path.isfile("./lyrics_dataframe.csv") == True:
        print(color.cyan+"lyrics_dataframe.csv"+color.green+" found\n"+color.end+"Adding lyrics of "+color.yellow+artist+color.end)
        lyrics_dataframe = pd.read_csv(
            "./lyrics_dataframe.csv", index_col=[0], encoding='utf-8')
        current_set = []
        for file in pathlib.Path(folder).iterdir():
            if file.is_file():
                current_song = []
                current_file = open(file, "r", encoding="utf-8")
                for line in current_file:
                    current_song.append(line+" ")
                current_song = "".join(current_song)
                current_set.append(current_song)
                current_file.close()
        current_set = pd.DataFrame(current_set, columns=['songs'])
        current_set["labels"] = artist
        lyrics_dataframe = pd.concat([lyrics_dataframe, current_set])
        lyrics_dataframe.reset_index(drop=True, inplace=True)
        lyrics_dataframe.to_csv("./lyrics_dataframe.csv")
        print("All lyrics in "+color.cyan+folder+color.end+" have been added to "+color.cyan+"lyrics_dataframe.csv" + color.end)
    else:
        print(color.cyan+"lyrics_dataframe.csv"+color.end +
              color.red+" not found\n"+color.end+"Creating new Dataframe with lyrics of "+color.yellow+artist+color.end)
        current_set = []
        for file in pathlib.Path(folder).iterdir():
            if file.is_file():
                current_song = []
                current_file = open(file, "r", encoding="utf-8")
                for line in current_file:
                    current_song.append(line+" ")
                current_song = "".join(current_song)
                current_set.append(current_song)
                current_file.close()
        current_set = pd.DataFrame(current_set, columns=['songs'])
        current_set["labels"] = artist
        current_set.to_csv("./lyrics_dataframe.csv", encoding='utf-8')
        print("All lyrics in "+color.cyan+folder+color.end+" have been added to "+color.cyan+"lyrics_dataframe.csv"+ color.end)

combine_lyrics(artist, folder)
