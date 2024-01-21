import requests
from bs4 import BeautifulSoup
import json
import re
import time
year = 1929
session_total = 2024 - year
base_url = "https://www.oscars.org/oscars/ceremonies/{year}"
movie_list = []
 

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
}

def searching_heading(searching_text):
    for element in group:
        title_rows = element.find_all('div', class_="view-grouping-header")
        for title_row in title_rows:
            print('title_row is ', title_row)
            if title_row.text == searching_text:
                award_row = element.find('div', class_="view-grouping-content")
                winner_sign = award_row.h3
                winner_row = award_row.find('div', class_="views-row-first")

                specific_winner = winner_row.find('h4').get_text(strip=True) 
                specific_movie = winner_row.find('span', class_="field-content").get_text(strip=True)
                
                print("For test= ",title_row.text)
                print("For test= ",winner_sign.text)
                print("Winner is", specific_winner)
                print("Movie is", specific_movie)
                award_item = specific_winner + "<br>" + specific_movie 
                print(award_item)
                return award_item
    
    print("-")
    return False
        
for i in range(session_total):

    print("Year is", year)
    print('URL is ', base_url.format(year=year))

    response = requests.get(base_url.format(year=year), headers=headers)
 
    soup = BeautifulSoup(response.content, "html.parser")
    group = soup.find_all('div', class_='view-grouping')
    searching_text="Actor"
    best_actor = searching_heading(searching_text)
    if best_actor == False:
        searching_text="Actor in a Leading Role"
        best_actor = searching_heading(searching_text)

    searching_text="Actress"
    best_actress = searching_heading(searching_text)
    if best_actress == False:
        searching_text="Actress in a Leading Role"
        best_actress = searching_heading(searching_text)

    searching_text="Directing"
    best_directing = searching_heading(searching_text)
    if best_directing == False:
        best_directing = "N/A"

    searching_text="Directing (Comedy Picture)"
    best_directing_comedy = searching_heading(searching_text)
    if best_directing_comedy == False:
        best_directing_comedy = "N/A"

    searching_text="Directing (Dramatic Picture)"
    best_directing_drama = searching_heading(searching_text)
    if best_directing_drama == False:
        best_directing_drama = "N/A"

    searching_text="Writing (Original Story)"
    best_writing_original= searching_heading(searching_text)
    if best_writing_original == False:
        best_writing_original = "N/A"

    searching_text="Writing (Screenplay)"
    best_writing_screenplay = searching_heading(searching_text)
    if best_writing_screenplay == False:
        best_writing_screenplay = "N/A"

    searching_text="Writing (Original Screenplay)"
    best_original_screenplay = searching_heading(searching_text)
    if best_original_screenplay == False:
        best_original_screenplay = "N/A"

    searching_text="Writing (Adaptation)"
    best_writing_adpation = searching_heading(searching_text)
    if best_writing_adpation == False:
        best_writing_adpation = "N/A"

    searching_text="Writing (Motion Picture Story)"
    best_writing_motion = searching_heading(searching_text)
    if best_writing_motion == False:
        best_writing_motion = "N/A"
     ##So many writing and screenplay awards   finally i give up, sorry. oscar too many different kind of writing and screenplay.
    searching_text="Writing (Screenplay--based on material from another medium)"
    best_writing_screenplay_1 = searching_heading(searching_text)
    if best_writing_screenplay_1 == False:
        best_writing_screenplay_1 = "N/A"
    
    searching_text="Writing (Story and Screenplay--written directly for the screen)"
    best_writing_screenplay_2 = searching_heading(searching_text)
    if best_writing_screenplay_2== False:
        best_writing_screenplay_2 = "N/A"

    searching_text="Writing (Screenplay Based on Material Previously Produced or Published)"
    best_writing_screenplay_3 = searching_heading(searching_text)
    if best_writing_screenplay_3== False:
        best_writing_screenplay_3 = "N/A" 

    searching_text="Outstanding Picture"
    best_film = searching_heading(searching_text)
    if best_film == False:
        searching_text="Outstanding Production"
        best_film = searching_heading(searching_text)
        if best_film ==False:
            searching_text="Outstanding Motion Picture"
            best_film = searching_heading(searching_text)
            if best_film ==False:
                searching_text="Best Motion Picture"
                best_film = searching_heading(searching_text)
                if best_film ==False:
                    searching_text="Best Picture"
                    best_film = searching_heading(searching_text)

    if best_actress:
        movie_list.append({
            "session": i+1,
            "year": year,
            "bestActor": best_actor,
            "bestActress": best_actress,
            "bestdirectingComedy": best_directing_comedy,
            "bestdirectingDrama": best_directing_drama,
            "bestdirecting": best_directing,
            "bestFilm": best_film,
        })  

    time.sleep(1)
    year += 1


                                      
with open("data.json", "w", encoding="utf-8") as jsonfile:
    json.dump(movie_list, jsonfile, ensure_ascii=False, indent=4)