from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, ForeignKey, Double, Enum

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(String,primary_key=True,nullable=False)
    feedback = Column(String,nullable=True)
    order_id = Column(String,nullable=False)
    user_id = Column(String,nullable=False)
    shop_id = Column(String,nullable=False)