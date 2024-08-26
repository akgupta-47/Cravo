from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, ForeignKey, Double, Enum
import enum 

class StatusEnum(enum.Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    
class PaymentMethod(enum.Enum):
    DCARD = 'debit_card'
    CCARD = 'credit_card'
    COD = 'cash_on_delivery'
    UPI = 'upi'
    
class Indicator(enum.Enum):
    DFC = 'debit_from_consumer'
    CTU = 'credit_to_user'

class Payment(Base):
    __tablename__ = "payments"

    id = Column(String,primary_key=True,nullable=False)
    status = Column(Enum(StatusEnum),nullable=False, server_default='PENDING')
    method = Column(Enum(PaymentMethod),nullable=False)
    amount = Column(Double,nullable=False)
    delivery = Column(Double,nullable=False) # delivery fee
    pfee = Column(Double,nullable=False) # platform fee
    user_id = Column(String,nullable=False)
    shop_id = Column(String,nullable=False)
    dc_indicator = Column(String,nullable=False, server_default='DFC')
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))