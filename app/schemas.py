from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, Literal


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # optional parameter if not provided then true


class PostCreate(PostBase):
    pass


class Post(PostBase):
    # title: str
    # content: str
    # published: bool #inherited
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True  # this will return the pydantic model if not provided then it will return dict results in error


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]  # direction 1 or 0
