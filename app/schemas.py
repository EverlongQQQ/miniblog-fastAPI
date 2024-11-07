from pydantic import BaseModel, EmailStr, Field, ConfigDict
from pydantic.types import conint
from typing_extensions import Annotated
from datetime import datetime
from typing import Optional

####### USER SCHEMAS #########
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

####### POST SCHEMAS #########
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    model_config = ConfigDict(from_attributes=True)

class PostOut(BaseModel):
    Post: Post
    votes: int

    model_config = ConfigDict(from_attributes=True)

####### TOKEN SCHEMAS #########
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenDate(BaseModel):
    id: int

####### VOTE SCHEMAS #########

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1)] # less or = to 1
