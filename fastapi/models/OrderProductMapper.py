from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, ForeignKey, Double, Enum

class OrderProductMapper(Base):
    __tablename__ = "order_product"

    id = Column(Integer,primary_key=True,nullable=False)
    product_id = Column(String,nullable=False)
    order_id = Column(String,nullable=False)
    quantity = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))