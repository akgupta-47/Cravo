# from database import Base
# from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, ForeignKey


# class Post(Base):
#     __tablename__ = "posts"

#     id = Column(Integer,primary_key=True,nullable=False)
#     title = Column(String,nullable=False)
#     content = Column(String,nullable=False)
#     published = Column(Boolean, server_default='TRUE')
#     created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    
# class Comments(Base):
#     __tablename__ = "comments"

#     id = Column(Integer,primary_key=True,nullable=False)
#     parent_id = Column(Integer,ForeignKey("posts.id"))
#     comment = Column(String)
from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))