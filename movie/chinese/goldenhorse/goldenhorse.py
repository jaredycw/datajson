import requests
from bs4 import BeautifulSoup
import json
import re

def table_function(variable_table, year):
    if variable_table:

        try:
            rows = variable_table.find_all("tr")
            heading = variable_table.find_all("th")
            marked_rows = [row for row in rows if "mark" in row.get("class", [])]
            tidy_heading = "".join([th.get_text(strip=True) for th in heading])
            tidy_marked_rows = "".join([mr.get_text(strip=True) for mr in marked_rows])

            tidy_heading = tidy_heading.replace("[<th colspan=\"2\">", "").replace("</th>]", "")
            print(year, " Heading is", tidy_heading)
            if marked_rows:
                row_with_td = marked_rows[0]  # Assuming only one marked row
                td_elements = row_with_td.find_all("td")
                if len(td_elements) >= 2:
                    tidy_content_0 = td_elements[0].get_text(strip=True)
                    if variable_table == bestFilm_table:
                        td_content_1 = td_elements[0].get_text(strip=True)
                        tidy_data = ""
                        tidy_content_0 = "《" + tidy_content_0 + "》"
                    else:
                        td_content_1 = td_elements[1].get_text(strip=True)
                        tidy_data = "《" + td_content_1 + "》"
                
                    ##tidy_marked_rows = tidy_content_0 + tidy_data + "-" + tidy_heading
                    tidy_marked_rows = tidy_content_0 + tidy_data
                    print(year,"Data is", tidy_marked_rows)
                    return tidy_marked_rows
                else:
                    print("Error: Not enough <td> elements in the marked row.")
                    
            else:
                print("Error: No marked rows found.")  
                tidy_marked_rows = "N/A"
                return tidy_marked_rows
            
            if tidy_marked_rows is not None:
                movie_list.append({tidy_heading: tidy_marked_rows})
        except:
            print("Error the table is not work")
            tidy_marked_rows = "N/A"
            return tidy_marked_rows
    
        return None
    else:
        tidy_marked_rows = "N/A"
        return tidy_marked_rows

def searching_heading(variable_table, searching_text):
    for table in tables:
        th_element = table.find("th")
        if th_element and searching_text in th_element.text:
            variable_table = table
    return variable_table

year = 1962
base_url = "https://www.goldenhorse.org.tw/awards/nw/?serach_type=award&sc=10&search_regist_year={year}&ins=0"
movie_list = []
best_film_list = []
best_director_list = []
best_actor_list = []
best_actress_list = []
best_screenplay_list = []
best_origin_screenplay_list = []
best_adpated_screenplay_list = []

best_original_screenplay = ""
best_adapted_screenplay = ""
bestFilm_table = ""
bestDirector_table = ""
bestActor_table = ""
bestActress_table = ""
bestScreenplay_table = ""
bestOriginalScreenplay_table = ""
bestAdaptedScreenplay_table = ""
for i in range(60):
   
    print("Year is ", year)
    ## 1964 因新聞局在台北剛主辦完亞洲影展，以及發生民航空難，該年度的金馬獎宣佈停辦一次[註 1]，故於隔年第3屆的金馬獎正式實施該辦法[4]。
    ## 1974 民國63年因臺北市舉辦1974年亞洲影展，金馬獎停辦一次
    if year == 1964 or year == 1974:
       year += 1

    response = requests.get(base_url.format(year=year))
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all("table")
    searching_text="最佳劇情片"
    bestFilm_table = searching_heading(bestFilm_table, searching_text)
    searching_text="最佳導演"
    bestDirector_table = searching_heading(bestDirector_table, searching_text)
    searching_text="最佳男主角"
    bestActor_table= searching_heading(bestActor_table, searching_text)
    searching_text="最佳女主角"
    bestActress_table= searching_heading(bestActress_table, searching_text)
    searching_text="最佳編劇"
    bestScreenplay_table= searching_heading(bestScreenplay_table, searching_text)

    
    if year > 1978:
        searching_text="最佳原著劇本"
        bestOriginalScreenplay_table = searching_heading(bestOriginalScreenplay_table, searching_text)
        searching_text="最佳改編劇本"
        bestAdaptedScreenplay_table = searching_heading(bestAdaptedScreenplay_table, searching_text)
        best_original_screenplay = table_function(bestOriginalScreenplay_table, year)
        best_adapted_screenplay = table_function(bestAdaptedScreenplay_table, year)
        
 
        

    best_film = table_function(bestFilm_table, year)
    best_director = table_function(bestDirector_table, year)
    best_actor = table_function(bestActor_table, year)
    best_actress = table_function(bestActress_table, year)
    best_screenplay = table_function(bestScreenplay_table, year)
    

    if best_film and best_director and best_actor and best_actress:
        movie_list.append({
            "session": i+1,
            "year": year,
            "bestFilm": best_film,
            "bestDirector": best_director,
            "bestActor": best_actor,
            "bestActress": best_actress,
            "bestScreenplay": best_screenplay,
            "bestOriginalScreenplay": best_original_screenplay,
            "bestAdaptedScreenplay": best_adapted_screenplay
        })
    
    year += 1


                                      
with open("data.json", "w", encoding="utf-8") as jsonfile:
    json.dump(movie_list, jsonfile, ensure_ascii=False, indent=4)