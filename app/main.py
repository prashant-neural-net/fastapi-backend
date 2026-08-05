from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import user, post

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

## connecting to the database
while True:
    try:
        conn = psycopg2.connect(
            host="127.0.0.1",
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


## root path
@app.get("/")
def root():
    return {"message": "jai mata di"}









