from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List, Annotated
from .. import schemas
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from .. database import engine, get_db


router = APIRouter(prefix="/posts", tags=['Posts'])


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[schemas.PostResponse]
)
def get_post(db: Session = Depends(get_db)):
    ## executing query
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()

    if posts is None:  # empty post
        return {"message": "No available posts"}

    else:
        return posts


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(
    #     """INSERT INTO posts (title, content, is_published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.is_published),
    # )
    # new_post = cursor.fetchone()
    print(curr_user.email)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse
)
def get_post_by_id(id: int, db: Session = Depends(get_db)):

    # cursor.execute("""SELECT * FROM posts where id = %s """, (id,))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    else:
        return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts where id = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):

    # cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s, is_published = %s WHERE id = %s RETURNING *""",
    #     (post.title, post.content, post.is_published, (id,)),
    # )

    # update_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post_update = post_query.first()

    if post_update == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()
