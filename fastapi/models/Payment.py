from sqlmodel import SQLModel, Field
from datetime import datetime
import enum 

class Status(enum.Enum):
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

class PaymentBase(SQLModel):
    status: Status
    method: PaymentMethod
    amount: float
    pfee: float
    delivery: float
    user_id: str
    shop_id: str
    dc_indicator: Indicator
    created_at: datetime = Field(default=datetime.UTC)

class Payment(PaymentBase, table=True):
    id = str = Field(default=None, primary_key=True)