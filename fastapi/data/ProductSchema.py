from datetime import datetime
from typing import Optional

import enums as productEnums
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """Base schema for product data validation."""

    name: Optional[str] = Field(None, description="Name of the product")
    description: Optional[str] = Field(None, description="Description of the product")
    country_of_origin: str = Field(
        ..., description="Country where the product is manufactured"
    )
    fssai: str = Field(..., description="FSSAI certification number")
    ingredients: Optional[str] = Field(
        None, description="List of ingredients in the product"
    )
    manufacturer: str = Field(..., description="Manufacturer of the product")
    manufacturer_address: str = Field(..., description="Address of the manufacturer")
    nutritional_info: Optional[str] = Field(
        None, description="Nutritional information of the product"
    )
    unit: str = Field(..., description="Unit of measurement (e.g., kg, ml, pcs)")
    shelf_life: Optional[str] = Field(None, description="Shelf life of the product")
    category: productEnums.Category = Field(..., description="Product category")
    sub_type: Optional[productEnums.SubCategory] = Field(
        None, description="Product sub-category"
    )
    status: Optional[str] = Field("1", description="Status of the product")


class ProductCreate(ProductBase):
    """Schema for creating a new product."""

    id: str = Field(..., description="Primary key, unique identifier for the product")


class ProductUpdate(ProductBase):
    """Schema for updating product details."""

    id: Optional[str] = Field(None, description="Product ID (optional for updates)")


class ProductResponse(ProductBase):
    """Schema for returning product details."""

    id: str
    created_at: datetime = Field(
        ..., description="Timestamp when the product was created"
    )

    class Config:
        orm_mode = True  # Enables conversion from SQLAlchemy models
