import enum

import enums as productEnums
from database import Base
from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    Double,
    Enum,
    ForeignKey,
    Integer,
    String,
    text,
)

""" <-
@Parent = [Product]
@Description = Database structure for all the product info storage
-> """


class Category(enum.Enum):
    FOOD = "food"
    STATIONARY = "stationary"
    ELECTRICAL = "electrical"
    PLUMBING = "plumbing"
    ELECTRONICS = "electronics"
    CLOTH = "cloth"
    BASIC = "basic"


class SubCategory(enum.Enum):
    BASIC = "basic"


class Product(Base):
    __tablename__ = "products"

    """ <-
    @Fields
    @PKeys = [id]
    @FKeys = []
    @Enums = [Product_Category,Product_SubCategory]
    -> """
    id = Column(String, primary_key=True, nullable=False)
    family_id = Column(String, nullable=True)
    image = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    country_of_origin = Column(String, nullable=False)
    fssai = Column(String, nullable=False)
    manufacturer = Column(String, nullable=False)
    ingredients = Column(String, nullable=True)
    manufacturer_address = Column(String, nullable=False)
    nutritional_info = Column(String, nullable=True)
    unit = Column(Double, nullable=False)
    price = Column(Double, nullable=False)
    weight = Column(Double, nullable=False)
    shelf_life = Column(String, nullable=True)
    category = Column(
        Enum(Category), nullable=False, server_default=Category.BASIC.value
    )
    sub_type = Column(
        Enum(SubCategory), nullable=True, server_default=SubCategory.BASIC.value
    )
    status = Column(String, nullable=True, server_default=1)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
