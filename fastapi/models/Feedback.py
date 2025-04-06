from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, ForeignKey, Double, Enum

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(String,primary_key=True,nullable=False)
    rating_order = Column(Integer,nullable=True)
    feedback_order = Column(String,nullable=True)
    rating_shop = Column(Integer,nullable=True)
    feedback_shop = Column(String,nullable=True)
    rating_delivery = Column(Integer,nullable=True)
    feedback_delivery = Column(String,nullable=True)
    shop_id = Column(String,nullable=False)
    order_id = Column(String,nullable=False)
    agent_id = Column(String,nullable=True)