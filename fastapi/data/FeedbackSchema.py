from typing import List, Optional, Union

from pydantic import UUID4, BaseModel


class Product(BaseModel):
    id: str  # ID can be None at creation but required later
    rating: Optional[int] = None
    feedback: Optional[str] = None


class FeedbackSchema(BaseModel):
    id: Optional[Union[str, UUID4]] = None  # Initially null but required later
    rating_order: Optional[int] = None
    feedback_order: Optional[str] = None
    rating_shop: Optional[int] = None
    feedback_shop: Optional[str] = None
    rating_delivery: Optional[int] = None
    feedback_delivery: Optional[str] = None
    shop_id: str
    agent_id: str
    order_id: str
    product_feedback: Optional[List[Product]] = None

    class Config:
        from_attributes = True
