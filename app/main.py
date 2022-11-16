from .routers import post, user, auth, vote
import enum
from pyexpat import model
from tokenize import String
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from sqlalchemy.orm import Session
from .database import engine, Session_api, get_db
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all()

app = FastAPI()


origins = ['*']
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


# Session talking with database

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='database_for_api',
#                                 user='postgres', password='database123', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Connected to database")
#         break
#     except Exception as error:
#         print("Error: ", error)
#         time.sleep(2)

my_posts = [{"id": 1, "title": "title of post1", "content": "content of post 1"}, {
    "id": 2, "title": "title of post2", "content": "content of post 2"}]

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():

    return {"Display this message": "Welcome to the sample api"}
