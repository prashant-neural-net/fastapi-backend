from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

# from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True


class PostCreate(PostBase):
    title: str
    content: str


class PostResponse(PostBase):

    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    user_id: int
    user: UserOut


class PostWithVotes(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    Post: PostResponse
    votes: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int


class VoteCreate(BaseModel):
    vote: int
    