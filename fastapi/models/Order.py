from sqlmodel import SQLModel, Field
from datetime import datetime

class OrderBase(SQLModel):
    total: float = Field(default_factory=0)
    track_id: str
    user_id: str
    shop_id: str
    created_at: datetime = Field(default=datetime.UTC)
    
class Order(OrderBase, table = True):
    id: str = Field(default=None, primary_key= True)
    