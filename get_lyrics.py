from utils.farben import color
import argparse
import re
import requests
from bs4 import BeautifulSoup
import os

parser = argparse.ArgumentParser(
    description="This program saves all lyrics of an artist to txt-files")
parser.add_argument("artist", help="artist-name", type=str)
parser.add_argument("url", help="URL of artist's page on lyrics.com", type=str)
args = parser.parse_args()
artist = args.artist
url = args.url

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'}

def to_file(filename, content, mode, encoding):
    f = open(filename, mode, encoding=encoding)
    f.write(content)
    f.close()
 
def extract_lyrics(artist, url):
    print("requesting "+color.yellow+artist+"'s"+color.end + " page at "+color.cyani+"lyrics.com"+color.end+" to find song-links...")
    page = requests.get(url, headers=headers)
    pattern = '/lyric/[A-z0-9/+%._-]+'
    prefix_url = 'https://www.lyrics.com'
    song_links = re.findall(
        pattern=pattern, string=page.text, flags=re.IGNORECASE)
    for song_link in song_links:
        link = prefix_url + song_link
        page = requests.get(link, headers=headers)
        song_soup = BeautifulSoup(page.text, "html.parser")
        lyric_body = song_soup.find_all(class_="lyric-body")
        text_only = [lyrics.get_text() for lyrics in lyric_body]
        lyrics = "".join(text_only)
        song_name = re.findall(pattern='([^\/]+)\/?$', string=song_link) 
        new_file = song_name[0]
        print("requesting" + color.yellow, new_file, color.end + "and saving lyrics to: " + color.cyan + "./" + artist + "_lyrics/{}.txt".format(new_file) + color.end)
        if os.path.isdir("./"+artist+"_lyrics/") == False: 
            os.mkdir("./"+artist+"_lyrics/")
        to_file('./'+artist+'_lyrics/{}.txt'.format(new_file),
            lyrics, "w", encoding="utf-8")

extract_lyrics(artist, url)
print("lyrics-files are in directory: " +color.cyan+artist+"_lyrics"+color.end)
