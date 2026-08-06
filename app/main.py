from fastapi import FastAPI, Response,HTTPException
from fastapi.params import Body
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine
from .routers import user, post, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

## connecting to the database
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="yash",
            password="password123",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        break

    except Exception as error:
        print("can't connect to the server....")
        print(error)
        time.sleep(2)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


## root path
@app.get("/")
def root():
    return {"message": "jai mata di"}
