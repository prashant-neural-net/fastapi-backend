from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import engine, get_db

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("/{post_id}", status_code=status.HTTP_201_CREATED)
def create_vote(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> str:
    post = db.get(models.Post, post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
        )
    like = db.get(models.Vote, (current_user.id, post_id))
    if like is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="post is already liked"
        )
    new_vote = models.Vote(user_id=current_user.id, post_id=post_id)
    db.add(new_vote)
    db.commit()

    return f"user: {current_user.id} liked post: {post_id}"


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vote(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    like = db.get(models.Vote, (current_user.id, post_id))
    if like is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"vote does not exist"
        )

    db.delete(like)
    db.commit()
    
    

    

    


