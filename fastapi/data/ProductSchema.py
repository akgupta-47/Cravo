from datetime import datetime
from enum import Enum
from typing import Optional, Union

from pydantic import UUID4, BaseModel, Field


class Category(str, Enum):
    FOOD = "food"
    STATIONARY = "stationary"
    ELECTRICAL = "electrical"
    PLUMBING = "plumbing"
    ELECTRONICS = "electronics"
    CLOTH = "cloth"
    BASIC = "basic"


class SubCategory(str, Enum):
    BASIC = "basic"


class ProductBase(BaseModel):
    id: Optional[Union[str, UUID4]] = None
    family_id: Optional[str] = None
    image: Optional[str] = None
    name: str
    description: Optional[str] = None
    country_of_origin: str
    fssai: str
    manufacturer: str
    ingredients: Optional[str] = None
    manufacturer_address: str
    nutritional_info: Optional[str] = None
    unit: float
    price: float
    weight: float
    shelf_life: Optional[str] = None
    category: Category = Field(default=Category.BASIC)
    sub_type: Optional[SubCategory] = Field(default=SubCategory.BASIC)
    status: Optional[str] = Field(default="1")
    created_at: Optional[datetime] = None


class ProductESearch(BaseModel):
    """Use this for updating existing product"""

    id: str
    family_id: str = None
    image: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    unit: Optional[float] = None
    weight: Optional[float] = None
    category: Optional[Category] = None
    sub_type: Optional[SubCategory] = None
    status: Optional[str] = None
