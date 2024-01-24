import requests
from bs4 import BeautifulSoup
import json
import re
import time
year = 1949
session_total = 2024 - year
base_url = "https://awards.bafta.org/award/{year}/film"
movie_list = []
 

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
}
 
def searching_heading(searching_text):
    count = 0

    for element in group_col:
        tables = element.find_all("li", class_="search-result-wrapper")
        for table in tables:
            result_title = table.find("div", class_="search-result-title")
            if result_title:
                count += 1
            winner = table.find("div", class_="search-result-winner")
            winnerDetailed = table.find("div", class_="search-result-subtitle search-result-winner")
            
            ##print("Result title is", result_title.text)
            ##print("Winner is", winner.p.get_text(strip=True))
            ##print("Awards in this year is", count)
            if result_title.get_text(strip=True) == searching_text:
                print("========================================")
                print("========================================")
                award_title = result_title.get_text(strip=True)
                print("Result title is ", result_title.get_text(strip=True) )
                winner_headline = winner.p.get_text(strip=True)
                print("Winner is ",  winner.p.get_text(strip=True))
                winner_subtitle = winnerDetailed.get_text(strip=True)
                print("Detail is ",winnerDetailed.get_text(strip=True))
                tidy_data =  winner_headline + "<br>" + winner_subtitle + " - " + award_title
                return tidy_data

    return "N/A"
        
for i in range(session_total):

    print("This year is ", year)
    print('URL is ', base_url.format(year=year))
    response = requests.get(base_url.format(year=year), headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    group_col = soup.find_all('ul')

    searching_text= "Film | British Actor in " + str(year)
    bestBritishActor = searching_heading(searching_text)

    searching_text= "Film | British Actress in " + str(year)
    bestBritishActress = searching_heading(searching_text)

    searching_text= "Film | British Film in " + str(year)
    bestBritishFilm = searching_heading(searching_text)
    if bestBritishFilm == "N/A":
        searching_text = "Film | British Film in " + str(year)
        bestBritishFilm = searching_heading(searching_text)
        if bestBritishFilm == "N/A":
            searching_text= "Film | Outstanding British Film in " + str(year)
            bestBritishFilm = searching_heading(searching_text)

    searching_text= "Film | Film in " + str(year)
    bestFilm = searching_heading(searching_text)
    if bestFilm == "N/A":
        searching_text= "Film | Best Film in " + str(year)
        bestFilm = searching_heading(searching_text)
        
        
    searching_text= "Film | Foreign Actor in " + str(year)
    bestForeignActor = searching_heading(searching_text)
    searching_text= "Film | Foreign Actress in " + str(year)
    bestForeignActress = searching_heading(searching_text)

    searching_text= "Film | Actor in " + str(year)
    bestActor = searching_heading(searching_text)
    if bestActor == "N/A":
        searching_text= "Film | Actor in a Leading Role in " + str(year)
        bestActor = searching_heading(searching_text)
        if bestActor == "N/A":
            searching_text= "Film | Leading Actor in " + str(year)
            bestActor = searching_heading(searching_text)

    searching_text= "Film | Actress in " + str(year)
    bestActress = searching_heading(searching_text)
    if bestActress == "N/A":
        searching_text= "Film | Actress in a Leading Role in " + str(year)
        bestActress = searching_heading(searching_text)
        if bestActress == "N/A":
            searching_text= "Film | Leading Actress in " + str(year)
            bestActress = searching_heading(searching_text)

    searching_text= "Film | Screenplay in " + str(year)
    bestScreenplay = searching_heading(searching_text)

    searching_text= "Film | Original Screenplay in " + str(year)
    bestOriginalScreenplay = searching_heading(searching_text)

    searching_text= "Film | Adapted Screenplay in " + str(year)
    bestAdaptedScreenplay = searching_heading(searching_text)

    searching_text= "Film | Direction in " + str(year)
    bestDirection = searching_heading(searching_text)
    if bestDirection == "N/A":
        searching_text= "Film | Director in " + str(year)
        bestDirection = searching_heading(searching_text)
    
    searching_text= "Film | Achievement in Direction in " + str(year)
    achievmentDirection = searching_heading(searching_text)
    searching_text = "Film | David Lean Award for Achievement in Direction in " + str(year)
    davidLeanDirection = searching_heading(searching_text)


    if searching_heading:
        movie_list.append({
            "session": i+1,
            "year": year,
            "bestBritishFilm": bestBritishFilm,
            "bestFilm": bestFilm,
            "bestBritishActor": bestBritishActor,
            "bestBritishActress": bestBritishActress,
            "bestForeignActor": bestForeignActor,
            "bestForeignActress": bestForeignActress,
            "bestActor": bestActor,
            "bestActress": bestActress,
            "bestScreenplay": bestScreenplay,
            "bestOriginalScreenplay": bestOriginalScreenplay,
            "bestAdaptedScreenplay": bestAdaptedScreenplay,
            "bestDirection": bestDirection,
            "achievmentDirection": achievmentDirection,
            "davidLeanDirection": davidLeanDirection,
        })  

    time.sleep(1)
    year += 1


                                      
with open("data.json", "w", encoding="utf-8") as jsonfile:
    json.dump(movie_list, jsonfile, ensure_ascii=False, indent=4)