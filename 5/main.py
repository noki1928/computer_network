import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from parser import Parser
from database import Database


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await asyncio.to_thread(database.close)
    await asyncio.to_thread(parser.close)


app = FastAPI(lifespan=lifespan)
parser = Parser()
database = Database()


@app.put("/parse")
def parse_page(url: str):
    films = parser.parse_page(url=url)
    database.save_to_db(films)
    return {"status": "success"}


@app.get("/get_data")
def get_data():
    rows = database.get_all_data()
    if not rows:
        return {"status": "empty"}
    
    return [
        {
            "title": row[0],
            "year": row[1],
            "rating": row[2],
            "link": row[3],
            "poster": row[4]
        }
        for row in rows
    ]


@app.get("/clean_db")
def clean_db():
    database.clean_db()
    return {"status": "success"}
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
