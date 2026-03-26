import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth


class Parser:
    def __init__(self) -> None:
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=options)
        stealth(self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
    
    def parse_page(self, url: str) -> list:
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'ul.poster-list.-p70.-grid')
                )
            )
            posters_container = self.driver.find_element(
                By.CSS_SELECTOR,
                'ul.poster-list.-p70.-grid'
            )
            films = posters_container.find_elements(
                By.CSS_SELECTOR, 
                'li.posteritem'
            )
            film_batch = []

            for film in films:
                current_film = film.find_element(By.CSS_SELECTOR, "a")
                current_poster = film.find_element(By.CSS_SELECTOR, "img")
                poster = current_poster.get_attribute("src")

                info = current_film.get_attribute("data-original-title").split()
                title = " ".join(info[:-2])
                year_with_brackets = info[-2]
                year = int(re.search(('[0-9]+'), year_with_brackets).group())
                rate = float(info[-1])
                link = current_film.get_attribute("href")

                film_batch.append((title, year, rate, link, poster))

            print("\t\tParsed page")
            return film_batch
        
        except Exception as e:
            print(f"Error: {e}")

    def close(self) -> None:
        self.driver.quit()

        



