from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, ForeignKey, Double, Enum

''' <-
@Parent = []
@Description = All the API spec related to Orders CRUD operations
@Table = Products
-> '''
class Order(Base):
    __tablename__ = "orders"

    ''' <-
    @Fields
    @PKeys = [id]
    @FKeys = []
    -> '''
    id = Column(String,primary_key=True,nullable=False)
    total = Column(Double,nullable=False)
    track_id = Column(String,nullable=False)
    user_id = Column(String,nullable=False)
    shop_id = Column(String,nullable=False)
    address_id  = Column(String,nullable=False)
    payment_id = Column(String,nullable=False)
    bid_id = Column(String,nullable=True)
    feedback_id = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    arrived_at = Column(TIMESTAMP(timezone=True))