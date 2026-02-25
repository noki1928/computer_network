import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

MAX_PAGE = 10
def parse_page(driver, films, res):
    for film in films:
        curr_film = film.find_element(By.CSS_SELECTOR, "a")
        curr_poster = film.find_element(By.CSS_SELECTOR, "img")
        poster = curr_poster.get_attribute("src")

        film_info = curr_film.get_attribute("data-original-title").split()
        film_name = " ".join(film_info[:-2])
        film_year = film_info[-2].replace("(", "").replace(")", "")
        film_rate = film_info[-1]
        link = curr_film.get_attribute("href")
        # print(film_name, film_year, film_rate)

        res.append([film_name, film_year, film_rate, link, poster])

res = [['film_name', 'film_year', 'film_rate', 'link', 'poster']]

options = Options()
options.add_argument(
    '--user-data-dir=C:\\Users\\astva\\AppData\\Local\\Google\\Chrome\\User Data\\Default')

driver = webdriver.Chrome(options=options)

url = 'https://letterboxd.com/films/popular/'
driver.get(url)

WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.poster-list.-p70.-grid')))

posters_container = driver.find_element(By.CSS_SELECTOR, 'ul.poster-list.-p70.-grid')
films = posters_container.find_elements(By.CSS_SELECTOR, 'li.posteritem')

parse_page(driver, films, res)

for page in range(2, MAX_PAGE + 1):
    url = f'https://letterboxd.com/films/popular/page/{page}/'
    driver.get(url)

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.poster-list.-p70.-grid')))

    posters_container = driver.find_element(By.CSS_SELECTOR, 'ul.poster-list.-p70.-grid')
    films = posters_container.find_elements(By.CSS_SELECTOR, 'li.posteritem')

    parse_page(driver, films, res)

driver.quit()


with open('results.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(res[0])
    writer.writerows(res[1:])