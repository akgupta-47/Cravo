from database import Base
from sqlalchemy import Column, String, TIMESTAMP, Boolean, text

class Test(Base):
    __tablename__ = "test"

    id = Column(String,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=True)
    published = Column(Boolean, server_default='FALSE')
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))