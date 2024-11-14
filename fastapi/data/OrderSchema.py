from typing import Dict, Union
from typing import List
from pydantic import BaseModel, Field
from uuid import UUID

# do we need offered price ??
class Product:
    id: str
    quantity: int
    available: bool

class Order(BaseModel):
    id: Union[str, UUID]
    total: float
    track_id: str
    user_id: str
    shop_id: str
    payment_id: str
    rating: int
    feedback: str
    products: List[Product]
    