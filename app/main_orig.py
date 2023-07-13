from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from datetime import datetime
import psycopg
from psycopg.rows import dict_row
import time

# from typing import Optional
from random import randrange


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    updated_at: datetime | None


while True:
    try:
        conn = psycopg.connect(
            host="localhost",
            dbname="fastapi",
            user="postgres",
            password="ado99rdo",
            row_factory=dict_row,
        )
        cursor = conn.cursor()
        print("Database connected!")
        break
    except Exception as err:
        print("Connection to database failed!")
        print("Error: ", err)
        time.sleep(2)

my_posts = [
    {"title": "Title of Post 1", "content": "Content of Post 1", "id": 1},
    {"title": "Title of Post 2", "content": "Content of Post 2", "id": 2},
]


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    sql = """SELECT *
               FROM posts"""
    cursor.execute(sql)
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    sql = """INSERT INTO posts (title, content, published)
               VALUES (%s, %s, %s)
              RETURNING *"""
    cursor.execute(sql, (payload.title, payload.content, payload.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    sql = """SELECT *
               FROM posts
              WHERE id = %s"""
    cursor.execute(sql, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"Post with id: {id} was not found"},
        )
    return {"data": post}


@app.delete("/posts/{id}")
def delete_post(id: int, res: Response):
    sql = """DELETE
               FROM posts
              WHERE id = %s
             RETURNING *"""
    cursor.execute(sql, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"Post with id: {id} was not found"},
        )
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    sql = """UPDATE posts
                SET title = %s,
                    content = %s,
                    published = %s,
                    updated_at = now()
              WHERE id = %s
             RETURNING *"""
    cursor.execute(sql, (post.title, post.content, post.published, str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"Post with id: {id} was not found"},
        )
    conn.commit()
    return {"data": post}
