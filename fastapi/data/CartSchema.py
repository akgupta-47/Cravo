from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class CartItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    price: float


class Fee(BaseModel):
    total: float
    platform_fee: float = 0
    surge: float = 0
    delivery: float
    tax: float
    discount: float = 0
    final: float


class Cart(BaseModel):
    user_id: str
    items: List[CartItem]
    fee: Fee
    coupon: str = None
    status: str = "active"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
