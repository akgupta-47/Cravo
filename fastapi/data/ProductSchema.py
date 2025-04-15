from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


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
    id: str
    family_id: str = None
    name: Optional[str] = None
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


class ProductCreate(ProductBase):
    """Use this when creating a new product"""

    pass


class ProductRead(ProductBase):
    """Use this for responses"""

    created_at: datetime

    class Config:
        orm_mode = True


class ProductUpdate(BaseModel):
    """Use this for updating existing product"""

    name: Optional[str] = None
    description: Optional[str] = None
    country_of_origin: Optional[str] = None
    fssai: Optional[str] = None
    manufacturer: Optional[str] = None
    ingredients: Optional[str] = None
    manufacturer_address: Optional[str] = None
    nutritional_info: Optional[str] = None
    unit: Optional[float] = None
    price: Optional[float] = None
    weight: Optional[float] = None
    shelf_life: Optional[str] = None
    category: Optional[Category] = None
    sub_type: Optional[SubCategory] = None
    status: Optional[str] = None


class ProductESearch(BaseModel):
    """Use this for updating existing product"""

    id: str
    family_id: str = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    weight: Optional[float] = None
    category: Optional[Category] = None
    sub_type: Optional[SubCategory] = None
    status: Optional[str] = None
