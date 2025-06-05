from database import Base
from sqlalchemy import Column, String, TIMESTAMP, text, Numeric, Enum
import enum 

# Enums
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

# Payment Model
class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, nullable=False)
    status = Column(Enum(StatusEnum), nullable=False, server_default=StatusEnum.PENDING.value)  # ✅ Fixed enum default
    method = Column(Enum(PaymentMethod), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)  # ✅ Fixed precision
    delivery = Column(Numeric(10, 2), nullable=False)  # ✅ Fixed precision
    pfee = Column(Numeric(10, 2), nullable=False)  # ✅ Fixed precision
    user_id = Column(String, nullable=False)
    shop_id = Column(String, nullable=False)
    dc_indicator = Column(Enum(Indicator), nullable=False, server_default=Indicator.DFC.value)  # ✅ Fixed enum default
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'))  # ✅ Correct default for timestamp
