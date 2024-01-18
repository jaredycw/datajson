import requests
from bs4 import BeautifulSoup
import re
import json
import time


url = "https://pitchfork.com/features/lists-and-guides/the-best-songs-of-the-1990s/"

song_list = []
label_list = []
order=250
label_order=250


response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

raws = soup.find_all("h2")
labels = soup.find_all("span", class_="caption__text")

print("raws:", len(raws))
print("labels", len(labels))

for label in labels:
    label_string = label
    label_regex = re.findall("[^\n]+", label_string.text)
    label = "".join(label_regex)
    label_list.append(label)
    if label_order == 97 + 1:
        label = "N/A"
        label_list.append(label)
        print("============label string ", label)
    print(label_order, "Label string is ", label)
    label_order-=1

for track, artist, year, label in zip( raws, raws, raws, label_list):
    
    track_text = track.text
    track_regex = re.findall("“(.*)”", track_text)
    track = "".join(track_regex)

    artist_text = artist.text
    artist_regex = re.findall("(.*?):", track_text)
    artist = "".join(artist_regex)

    year_text = year.text
    year_regex = re.findall("\((\d{4})\)", year_text)
    year = "".join(year_regex)
    song_list.append({"ranking": order, "track": track, "artist": artist, "year": year, "label": label})
    order-=1

with open("1990.json", "w", encoding="utf-8") as jsonfile:
    json.dump(song_list, jsonfile, ensure_ascii=False, indent=4)