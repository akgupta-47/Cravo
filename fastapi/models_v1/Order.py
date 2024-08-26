from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, ForeignKey, Double, Enum

class Order(Base):
    __tablename__ = "orders"

    id = Column(String,primary_key=True,nullable=False)
    total = Column(Double,nullable=False)
    track_id = Column(String,nullable=False)
    user_id = Column(String,nullable=False)
    shop_id = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))