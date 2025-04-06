# from typing import List
# from pydantic import BaseModel

# class CommentsBase(BaseModel):
#     comment: str
    
#     class Config:
#         from_attributes = True

# class PostBase(BaseModel):
#     content: str
#     title: str
#     comments: List[CommentsBase]

#     class Config:
#         from_attributes = True


# class CreatePost(PostBase):
#     class Config:
#         from_attributes = True
from pydantic import BaseModel

class PostBase(BaseModel):
    content: str
    title: str

    class Config:
        from_attributes = True

class CreatePost(PostBase):
    class Config:
        from_attributes = True