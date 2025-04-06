from database import Base
from sqlalchemy import Column, String, TIMESTAMP, Boolean, text
from sqlalchemy.schema import PrimaryKeyConstraint

class OrderProductMapper(Base):
    __tablename__ = "order_product"

    product_id = Column(String, nullable=False)
    order_id = Column(String, nullable=False)
    quantity = Column(String, nullable=False)
    available = Column(Boolean, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

    # Ensure __table_args__ is correctly formatted as a tuple
    __table_args__ = (
        PrimaryKeyConstraint('product_id', 'order_id'),
    )
