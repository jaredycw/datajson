from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re

pages = []
song_list = []
year = 1958
session_total = 2023 - year
base_url = "https://www.grammy.com/awards/"


chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
driver = webdriver.Chrome(options=chrome_options)


bestAlbum = ""
bestSong = ""
bestRecord = ""
newArtist = ""

wait = WebDriverWait(driver, 10)
 
print("Start scraping the tracks")

for i in range(1, session_total ):

    try:
        session = i
        if session % 10 == 1 and session % 100 != 11:
            ordinal = "st"
        elif session % 10 == 2 and session % 100 != 12:
            ordinal = "nd"
        elif session % 10 == 3 and session % 100 != 13:
            ordinal = "rd"
        else:
            ordinal = "th"
        if session > 59:
            url = base_url + str(session) + ordinal + "-annual-grammy-awards-" + str(year)
        else:
            url = base_url + str(session) + ordinal + "-annual-grammy-awards"
        driver.get(url)
        
        print("Year is", session)
        print('URL is', url)

        # Wait for the elements to be loaded
        wait = WebDriverWait(driver, 30)

        # Wait for the elements to be loaded
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".text-left.font-polaris.uppercase")))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".h-full.w-full.flex.flex-col.items-center.mt-6")))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mb-15px.text-center .w-full.text-center.font-polaris.font-bold.tracking-wider")))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mb-15px.text-center .awards-category-link a")))

        section = driver.find_elements(By.CSS_SELECTOR, ".h-full.w-full.flex.flex-col.items-center.mt-6")
        award_titles = driver.find_elements(By.CSS_SELECTOR, ".text-left.font-polaris.uppercase")
        winner_song = driver.find_elements(By.CSS_SELECTOR, ".mb-15px.text-center .w-full.text-center.font-polaris.font-bold.tracking-wider")
        artist_element = driver.find_elements(By.CSS_SELECTOR, ".mb-15px.text-center .awards-category-link a")
        new_artist_element = driver.find_elements(By.CSS_SELECTOR, ".mb-15px.text-center .text-center.font-polaris.tracking-wider")
    
        for j in range(len(section)):
            if award_titles[j].text == "ALBUM OF THE YEAR":
                print("ALBUM OF THE YEAR is", winner_song[j].text)
                winner = winner_song[j].text
                tidy_winner = winner.replace("\"", "")

                if j < len(artist_element):
                    bestAlbum = tidy_winner + " - " + artist_element[j].text
                else:
                    # Handle the case when j is out of range
                    artist_element = "No artist found"
                    bestAlbum = tidy_winner + " - " + artist_element
                print("==========================================")
            
            if award_titles[j].text == "RECORD OF THE YEAR":
                print("RECORD OF THE YEAR is", winner_song[j].text)
                winner = winner_song[j].text
                tidy_winner = winner.replace("\"", "")
                if j < len(artist_element):
                    bestRecord = tidy_winner + " - " + artist_element[j].text
                else:
                    # Handle the case when j is out of range
                    artist_element = "No artist found"
                    bestRecord = tidy_winner + " - " + artist_element
                print("==========================================")
            
            if award_titles[j].text == "SONG OF THE YEAR":
                print("SONG OF THE YEAR is", winner_song[j].text)
                winner = winner_song[j].text
                tidy_winner = winner.replace("\"", "")
                if j < len(artist_element):
                    bestSong = tidy_winner
                else:
                    # Handle the case when j is out of range
                    artist_element = "No artist found"
                    bestSong = tidy_winner + " - " + artist_element
                print("==========================================")
            
            if award_titles[j].text == "BEST NEW ARTIST":
                new_artist_element = new_artist_element[j].text
                tidy_new_artist_element = new_artist_element.replace("\"", "")
                if new_artist_element:
                    print("tidy new is", tidy_new_artist_element)
                    newArtist = tidy_new_artist_element
                else:
                    newArtist = "N/A"
                print("==========================================")

        year += 1
    except:
        print("stop in session", session)
        
    song_list.append({
            "session": session,
            "year": year,
            "bestRecord": bestRecord,
            "bestAlbum": bestAlbum,
            "bestSong": bestSong,
            "newArtist": newArtist,
        })    
    
   

    
 
# Close the webdriver
driver.quit()

# Save the data to a JSON file
with open("list.json", "w", encoding="utf-8") as jsonfile:
    json.dump(song_list, jsonfile, ensure_ascii=False, indent=4)
    print('finished all')
