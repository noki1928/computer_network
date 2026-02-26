import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


MAX_PAGE = 4

# Глобальный список для результатов парсинга (будет записан в CSV)
film_data_rows = [
    ['film_name', 'film_year', 'film_rate', 'link', 'poster']
]

options = Options()
options.add_argument(
    '--user-data-dir=C:\\Users\\astva\\AppData\\Local\\Google\\Chrome\\User Data\\Default'
    ) # Путь к папке с cookies

driver = webdriver.Chrome(options=options)


def driver_get_page(url: str) -> list:
    """Получает данные с одной страницы и возвращает список с данными фильмов"""
    driver.get(url)

    WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.poster-list.-p70.-grid')))

    posters_container = driver.find_element(By.CSS_SELECTOR, 'ul.poster-list.-p70.-grid')
    films = posters_container.find_elements(By.CSS_SELECTOR, 'li.posteritem')

    return films


def parse_page(films: list) -> list:
    """Парсит данные с одной страницы и добавляет их в список с данными фильмов"""
    for film in films:
        current_film = film.find_element(By.CSS_SELECTOR, "a")
        current_poster = film.find_element(By.CSS_SELECTOR, "img")
        poster_link = current_poster.get_attribute("src")

        film_info = current_film.get_attribute("data-original-title").split()
        film_name = " ".join(film_info[:-2])
        film_year = film_info[-2].replace("(", "").replace(")", "")
        film_rate = film_info[-1]
        letterboxd_link = current_film.get_attribute("href")
        # print(film_name, film_year, film_rate) # Раскомментировать для отображения фильмов в консоли

        film_data_rows.append([film_name, film_year, film_rate, letterboxd_link, poster_link])

try:
    url = 'https://letterboxd.com/films/popular/'
    films = driver_get_page(url=url)
    parse_page(films=films)

    for page in range(2, MAX_PAGE + 1):
        url = f'https://letterboxd.com/films/popular/page/{page}/'
        films = driver_get_page(url=url)
        parse_page(films=films)
finally:
    driver.quit()


with open('results.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(film_data_rows)
