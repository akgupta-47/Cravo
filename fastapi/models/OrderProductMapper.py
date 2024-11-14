from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, ForeignKey, Double, Enum
from sqlalchemy.schema import PrimaryKeyConstraint

class OrderProductMapper(Base):
    __tablename__ = "order_product"

    product_id = Column(String,nullable=False)
    order_id = Column(String,nullable=False)
    quantity = Column(String,nullable=False)
    available = Column(Boolean,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    
    __table_args_ = (
        PrimaryKeyConstraint('product_id','order_id','quantity')
    )