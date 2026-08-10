from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import engine, get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist",
        )

    return user


@router.get(
    "/{user_id}/posts",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.PostBase],
)
def get_all_post_of_user(
    user_id: int,
    db: Session = Depends(get_db),
):

    posts = db.query(models.Post).filter(models.Post.user_id == user_id).all()

    return posts
