from typing import List, Union
from fastapi import FastAPI
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
import models.Post
import schemas.PostSchema as postSchema
import models
from database import Base, engine, get_db
import schemas.ItemSchema as item
from routers.OrdersRouter import order_router

from dotenv import load_dotenv

load_dotenv() 

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(order_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: item.Item):
    return {"item_name": item.name, "item_id": item_id}

# @app.get("/posts/{post_id}")
# async def get_post(post_id: int, db: Session = Depends(get_db)):
#     result = db.query(models.Post).filter(models.Post.id == post_id).first()
#     if not result:
#         raise HTTPException(status_code=404, detail="post not found")
#     return result

# @app.get("/comments/{post_id}")
# async def get_comments(post_id: int, db: Session = Depends(get_db)):
#     result = db.query(models.Post).filter(models.Comments.parent_id == post_id).all()
#     if not result:
#         raise HTTPException(status_code=404, detail="comments not found")
#     return result

# @app.post("/posts/new")
# async def new_post(post: schemas.PostBase, db: Session = Depends(get_db)):
#     db_post = models.Post(content = post.content, title = post.title)
#     db.add(db_post)
#     db.commit()
#     db.refresh(db_post)
#     for comment in post.comments:
#         db_comment = models.Comments(comment = comment.comment, parent_id = db_post.id)
#         db.add(db_comment)
#     db.commit()