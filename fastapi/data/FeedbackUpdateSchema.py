from typing import List, Optional, Union

from pydantic import UUID4, BaseModel


class ProductUpdateSchema(BaseModel):
    product_id: Optional[str] = None  # Use 'product_id' for clarity
    rating: Optional[int] = None
    feedback: Optional[str] = None


class FeedbackUpdateSchema(BaseModel):
    id: Union[str, UUID4]  # ID should be required for updating
    rating_order: Optional[int] = None
    feedback_order: Optional[str] = None
    rating_shop: Optional[int] = None
    feedback_shop: Optional[str] = None
    rating_delivery: Optional[int] = None
    feedback_delivery: Optional[str] = None
    product_feedback: Optional[List[ProductUpdateSchema]] = None  # Nested updates

    class Config:
        from_attributes = True
