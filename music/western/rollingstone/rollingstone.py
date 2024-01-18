from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re

pages = []
song_list = []

chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.rollingstone.com/music/music-lists/best-songs-of-all-time-1224767/')

wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, 'pmc-gallery-list-nav-bar-render')))

links = element.find_elements(By.TAG_NAME, 'a')
hrefs = [link.get_attribute('href') for link in links]
print("Finding the pages first")

for href in hrefs:

    raw_link = re.findall("1224767/(.*)", href)
    href = "".join(raw_link)
    pages.append(href)

print("Appended all the pages")
print("Start scraping the tracks")

for i in range(len(pages)):
    url = 'https://www.rollingstone.com/music/music-lists/best-songs-of-all-time-1224767/' + pages[i]

    # Load the initial page
    driver.get(url)

    # Wait for the elements to be loaded
    wait = WebDriverWait(driver, 20)
    songs = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.c-gallery-vertical__slide-wrapper')))
    rank = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.c-gallery-vertical-album__number')))
    raw = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.c-gallery-vertical-album__title')))
    year = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.rs-list-item--year')))

    for j in range(len(songs)):
        artist = re.sub(", ‘([^']+)’", "", raw[j].text)
        raw2 = re.findall("‘([^']+)’", raw[j].text)
        track = "".join(raw2)
        song_list.append({"ranking": rank[j].text, "raw": raw[j].text, "track": track, "artist": artist, "year": year[j].text})      
        print('finished ', j)
        
print('Pages: ', i + 1)
            
# Close the webdriver
driver.quit()

# Save the data to a JSON file
with open("list.json", "w", encoding="utf-8") as jsonfile:
    json.dump(song_list, jsonfile, ensure_ascii=False, indent=4)
    print('finished all')