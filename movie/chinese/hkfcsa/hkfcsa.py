import requests
from bs4 import BeautifulSoup
import json
import re

base_url = "https://www.filmcritics.org.hk/node/2593/"
movie_list = []
url = base_url
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
table = soup.find('table')

def looping_list(target, target_list, target_name, relative_list, award_session_list):
    for target in target_list:
        duplicate_entry = next((entry for entry in relative_list if entry["sessionNumber"] == award_session_list[0]), None)
        if duplicate_entry:
            duplicate_entry[str(target_name)] = target
        else:
            relative_list.append({str(target_name): target})

for i in range(30):
    if table:
        rows = table.find_all("tr")
 
        if rows:
            award_session_list =[re.sub(r"\d+\r\n\t+", "", session.text.strip()) for session in rows[0].find_all("td")]
            award_setting_list = []
            best_films_list = []
            best_directors_list = []
            best_screenplay_list = []
            best_actors_list= []
            best_actress_list= []
            year_list = []
            
            session = rows[i+1].find_all("td")[0]
            award = rows[i+1].find_all("td")[1]
            print(award.text.strip())
            award_setting_list.append(award.text.strip())

            sessionNumber = re.sub(r"\d+\r\n\t+", "", session.text.strip())
            award_session_list.append(sessionNumber)

            year = re.sub(r"\D+", "", session.text.strip())
            year_list.append(year)

            pattern = r"最佳電影：(.+)\r"
            result = re.search(pattern, award.text.strip())
            if result:
                bestFilm = result.group(1)
                best_films_list.append(bestFilm)

            pattern = r"最佳導演：(.+)\r"
            result = re.search(pattern, award.text.strip())
            if result:
                bestDirector = result.group(1)
                best_directors_list.append(bestDirector)
            
            pattern = r"最佳編劇：(.+)\r"
            result = re.search(pattern, award.text.strip())
            if result:
                bestScreenplay = result.group(1)
                best_screenplay_list.append(bestScreenplay)

            pattern = r"最佳男演員：(.+)\r"
            result = re.search(pattern, award.text.strip())
            if result:
                bestActor = result.group(1)
                best_actors_list.append(bestActor)

            pattern = r"最佳女演員：(.+)"
            result = re.search(pattern, award.text.strip())
            if result:
                bestActress = result.group(1)
                best_actress_list.append(bestActress)

            field_name = "sessionNumber"
            looping_list(sessionNumber, award_session_list, field_name, movie_list, award_session_list)
            field_name = "year"
            looping_list(year, year_list, field_name, movie_list, award_session_list)
            field_name = "bestFilm"
            looping_list(bestFilm, best_films_list, field_name, movie_list, award_session_list)
            field_name = "bestDirector"
            looping_list(bestDirector, best_directors_list, field_name, movie_list, award_session_list)
            field_name = "bestScreenplay"
            looping_list(bestScreenplay, best_screenplay_list, field_name, movie_list, award_session_list)
            field_name = "bestActor"
            looping_list(bestActor, best_actors_list, field_name, movie_list, award_session_list)
            field_name = "bestActress"
            looping_list(bestActress, best_actress_list, field_name, movie_list, award_session_list)
            ##field_name = "award"
            ##looping_list(award, award_setting_list, field_name, movie_list, award_session_list)
            
with open("data.json", "w", encoding="utf-8") as jsonfile:
    json.dump(movie_list, jsonfile, ensure_ascii=False, indent=4)