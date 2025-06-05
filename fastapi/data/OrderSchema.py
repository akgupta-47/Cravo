from typing import Union
from typing import List
from pydantic import BaseModel
from uuid import UUID

# do we need offered price ??
class Product(BaseModel):
    id: str
    quantity: int
    available: bool

class Order(BaseModel):
    id: Union[str, UUID]
    total: float
    track_id: str
    user_id: str
    shop_id: str
    address_id: str
    payment_id: str
    status: str
    bid_id: int
    feedback_id: str
    products: List[Product]
    arrived_at: str
    
    class Config:
        from_attributes = True
    