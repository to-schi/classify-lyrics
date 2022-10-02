"""
Command line tool to scrape lyrics from lyrics.com
"""
import argparse
import os
import re

import requests
from bs4 import BeautifulSoup

from utils.farben import Color

parser = argparse.ArgumentParser(
    description="This program saves all lyrics of an artist to txt-files"
)
parser.add_argument("artist", help="artist-name", type=str)
parser.add_argument("url", help="URL of artist's page on lyrics.com", type=str)
args = parser.parse_args()
ARTIST = args.artist
URL = args.url

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"
}


def to_file(filename, content, mode, encoding):
    """writes to file :)"""
    file = open(filename, mode, encoding=encoding)
    file.write(content)
    file.close()


def extract_lyrics(artist, url):
    """scrapes lyrics from lyrics.com-page"""
    print(
        "requesting "
        + Color.yellow
        + artist
        + "'s"
        + Color.end
        + " page at "
        + Color.cyani
        + "lyrics.com"
        + Color.end
        + " to find song-links..."
    )
    page = requests.get(url, headers=headers)
    pattern = "/lyric/[A-z0-9/+%._-]+"
    prefix_url = "https://www.lyrics.com"
    song_links = re.findall(pattern=pattern, string=page.text, flags=re.IGNORECASE)
    for song_link in song_links:
        link = prefix_url + song_link
        page = requests.get(link, headers=headers)
        song_soup = BeautifulSoup(page.text, "html.parser")
        lyric_body = song_soup.find_all(class_="lyric-body")
        text_only = [lyrics.get_text() for lyrics in lyric_body]
        lyrics = "".join(text_only)
        song_name = re.findall(pattern="([^\/]+)\/?$", string=song_link)  # type: ignore
        new_file = song_name[0]
        print(
            "requesting" + Color.yellow,
            new_file,
            Color.end
            + "and saving lyrics to: "
            + Color.cyan
            + "./"
            + artist
            + "_lyrics/{}.txt".format(new_file)
            + Color.end,
        )
        if os.path.isdir("./" + artist + "_lyrics/") is False:
            os.mkdir("./" + artist + "_lyrics/")
        to_file(
            "./" + artist + "_lyrics/{}.txt".format(new_file),
            lyrics,
            "w",
            encoding="utf-8",
        )


extract_lyrics(ARTIST, URL)
print("lyrics-files are in directory: " + Color.cyan + ARTIST + "_lyrics" + Color.end)
