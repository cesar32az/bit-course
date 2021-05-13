from pydantic import BaseModel
from typing import Optional, List


class BlogBase(BaseModel):
    title: str
    body: str
    published: Optional[bool]

class Blog(BlogBase):
    class Config():
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []

    class Config():
        orm_mode = True

class Creator(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True

class ShowBlog(BaseModel):
    title: str
    body: str
    creator: Creator

    class Config():
        orm_mode = True 

class Login(BaseModel):
    email: str
    password: str