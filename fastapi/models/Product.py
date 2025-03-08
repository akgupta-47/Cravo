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


class Product(Base):
    __tablename__ = "products"

    """ <-
    @Fields
    @PKeys = [id]
    @FKeys = []
    @Enums = [Product_Category,Product_SubCategory]
    -> """
    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    country_of_origin = Column(String, nullable=False)
    fssai = Column(String, nullable=False)
    ingredients = Column(String, nullable=True)
    manufacturer = Column(String, nullable=False)
    manufacturer_address = Column(String, nullable=False)
    nutritional_info = Column(String, nullable=True)
    unit = Column(String, nullable=False)
    shelf_life = Column(String, nullable=True)
    category = Column(Enum(productEnums.Category), nullable=False)
    sub_type = Column(Enum(productEnums.SubCategory), nullable=True)
    status = Column(String, nullable=True, server_default=1)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
