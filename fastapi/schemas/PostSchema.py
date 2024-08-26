from typing import List
from pydantic import BaseModel

class CommentsBase(BaseModel):
    comment: str
    
    class Config:
        orm_mode = True

class PostBase(BaseModel):
    content: str
    title: str
    comments: List[CommentsBase]

    class Config:
        orm_mode = True


class CreatePost(PostBase):
    class Config:
        orm_mode = True