import requests
from bs4 import BeautifulSoup
import json
import re

def looping_list(target, target_list, target_name, relative_list, sessions_title):
    for target in target_list:
        duplicate_entry = next((entry for entry in relative_list if entry["session"] == sessions_title[0]), None)
        if duplicate_entry:
            duplicate_entry[str(target_name)] = target
        else:
            relative_list.append({str(target_name): target})

def scrape_hkfa_awards(start_year, end_year):
    base_url = "https://www.hkfaa.com/winnerlist{:02d}.html"
    movie_list = []
    th = 2

    for i in range(start_year, end_year + 1):
        url = base_url.format(i)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find(id="table")
        year = 1982 + i - 1  # Calculate the year based on the index

        if table:
            rows = table.find_all("tr")

            if rows:
                award_sessions = [re.sub(r"\n.+", "", session.text.strip()) for session in rows[0].find_all("td")]
                best_films_list = []
                best_directors_list = []
                best_screenplay_list = []
                best_actors_list= []
                best_actress_list= []
                year_list = []
                session_list = []

                session = ""
                bestFilm = ""
                bestDirector = ""
                bestScreenPlay = ""
                bestActress = ""
                bestActor = ""

                if i == 1:
                    try:
                        best_film = rows[th+1].find_all("td")[1]
                        best_director = rows[th+2].find_all("td")[1]
                        bestScreenPlay = rows[th+3].find_all("td")[1]
                        best_actor = rows[th+4].find_all("td")[1]
                        best_actress = rows[th+5].find_all("td")[1]
                        best_films_list.append(best_film.text.strip())
                        best_directors_list.append(best_director.text.strip())
                        best_screenplay_list.append(bestScreenPlay.text.strip())
                        best_actors_list.append(best_actor.text.strip())
                        best_actress_list.append(best_actress.text.strip())
                        year_list.append(year)
                        session_list.append(i)
                    except (IndexError, KeyError):
                        print("Error in first session")
                if i > 1:
                    try:
                        best_film = rows[th+1].find_all("td")[2]
                        best_director = rows[th+2].find_all("td")[2]
                        bestScreenPlay = rows[th+6].find_all("td")[2]

                        best_actor = rows[th+3].find_all("td")[2]
                        best_actress = rows[th+4].find_all("td")[2]

                        tidy_best_director = re.sub(r"\n.*", "", best_director.text.strip())
                        tidy_best_screenplay = re.sub(r"\n.*", "", bestScreenPlay.text.strip())

                        tidy_best_actor = re.sub(r"\n.*", "", best_actor.text.strip())
                        tidy_best_actress = re.sub(r"\n.*", "", best_actress.text.strip())

                        if i > 3:
                            bestScreenPlay = rows[th+8].find_all("td")[2]
                            tidy_best_screenplay = re.sub(r"\n.*", "", bestScreenPlay.text.strip())

                        if i > 7:
                            bestScreenPlay = rows[th+3].find_all("td")[2]
                            best_actor = rows[th+4].find_all("td")[2]
                            best_actress = rows[th+5].find_all("td")[2]

                            tidy_best_director = re.sub(r"\n.*", "", best_director.text.strip())
                            tidy_best_screenplay = re.sub(r"\n.*", "", bestScreenPlay.text.strip())
                            tidy_best_actor = re.sub(r"\n.*", "", best_actor.text.strip())
                            tidy_best_actress = re.sub(r"\n.*", "", best_actress.text.strip())

                        tidy_best_film = re.sub(r"\n.*", "", best_film.text.strip())
                        best_films_list.append(tidy_best_film)

                        best_directors_list.append(tidy_best_director)
                        best_screenplay_list.append(tidy_best_screenplay)
                        best_actors_list.append(tidy_best_actor)
                        best_actress_list.append(tidy_best_actress)
                        
                        year_list.append(year)
                        session_list.append(i)
                    except (IndexError, KeyError):
                        print("Error after first session")

                field_name = "session"
                looping_list( session, award_sessions, field_name, movie_list, award_sessions)     
                field_name = "sessionNumber"
                looping_list( i, session_list, field_name, movie_list, award_sessions)  
                field_name = "year"
                looping_list( year, year_list, field_name, movie_list, award_sessions)                    
                field_name = "bestFilm"
                looping_list( bestFilm, best_films_list, field_name, movie_list, award_sessions)
                field_name = "bestDirector"
                looping_list( bestDirector, best_directors_list, field_name, movie_list, award_sessions)
                field_name = "bestScreenPlay"
                looping_list( bestScreenPlay, best_screenplay_list, field_name, movie_list, award_sessions)
                field_name = "bestActor"
                looping_list( bestActor, best_actors_list, field_name, movie_list, award_sessions)
                field_name = "bestActress"
                looping_list( bestActress, best_actress_list, field_name, movie_list, award_sessions)
                                               
    return movie_list

movie_list = scrape_hkfa_awards(1, 41)

with open("data.json", "w", encoding="utf-8") as jsonfile:
    json.dump(movie_list, jsonfile, ensure_ascii=False, indent=4)