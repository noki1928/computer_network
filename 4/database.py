from psycopg2 import connect
from psycopg2.extras import execute_values

import config


class Database:
    def __init__(self) -> None:
        self._connection = connect(
            database='films', 
            user=config.POSTGRES_USER, 
            password=config.POSTGRES_PASSWORD, 
            host='100.84.15.10', 
            port=5432
        )

        self._cursor = self._connection.cursor()

    def get_all_data(self) -> list:
        self._cursor.execute("SELECT * FROM films_from_letterboxd")
        print("\t\tGot data from db")
        return self._cursor.fetchall()
        
    
    def save_to_db(self, film_batch: list) -> None:
        if not film_batch:
            return
        execute_values(self._cursor, 
                    "INSERT INTO films_from_letterboxd "
                    "(title, year, rating, link, poster) VALUES %s", 
                    film_batch)
        self._connection.commit()
        print("\t\tSaved to db")

    def clean_db(self) -> None:
        self._cursor.execute("DELETE FROM films_from_letterboxd")
        self._connection.commit()
        print("\t\tCleaned db")

    def close(self) -> None:
        self._cursor.close()
        self._connection.close()
