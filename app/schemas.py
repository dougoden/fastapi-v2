from pydantic import BaseModel, conint, EmailStr
from datetime import datetime
from typing import List


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    updated_at: datetime | None


class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True


class UserLogin(UserBase):
    pass


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    updated_at: datetime | None


class Post(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime | None
    owner_id: int
    owner: User

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None


class VoteCreate(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)


class Vote(BaseModel):
    post_id: int
    user_id: int
