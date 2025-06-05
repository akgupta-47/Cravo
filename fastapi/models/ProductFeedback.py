from database import Base
from sqlalchemy import Column, Integer, PrimaryKeyConstraint, String

class ProductFeedback(Base):
    __tablename__ = "product_feedback"

    feedback_id = Column(String,nullable=False)
    product_id = Column(String,nullable=False)
    rating_product = Column(Integer,nullable=True)
    feedback_product = Column(String,nullable=True) 
    
    __table_args__ = (
        PrimaryKeyConstraint('product_id', 'feedback_id'),
    )
    