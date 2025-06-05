import enum

# import enums as productEnums
from database import Base
from sqlalchemy import TIMESTAMP, Column, Double, Enum, String, text

""" <-
@Parent = [Product]
@Description = Database structure for all the product info storage
-> """


class Category(enum.Enum):
    FOOD = "FOOD"
    STATIONARY = "STATIONARY"
    ELECTRICAL = "ELECTRICAL"
    PLUMBING = "PLUBING"
    ELECTRONICS = "ELECTRONICS"
    CLOTH = "CLOTH"
    BASIC = "BASIC"


class SubCategory(enum.Enum):
    BASIC = "BASIC"


class Product(Base):
    __tablename__ = "products"

    """ <-
    @Fields
    @PKeys = [id]
    @FKeys = []
    @Enums = [Product_Category,Product_SubCategory]
    -> """
    # Primary Key
    id = Column(String, primary_key=True, nullable=False)

    # Optional Foreign Key-style grouping (not enforced)
    family_id = Column(String, nullable=True)

    # Required Fields
    image = Column(String, nullable=False)
    name = Column(String, nullable=False)
    country_of_origin = Column(String, nullable=False)
    fssai = Column(String, nullable=False)
    manufacturer = Column(String, nullable=False)
    manufacturer_address = Column(String, nullable=False)
    unit = Column(Double, nullable=False)
    price = Column(Double, nullable=False)
    weight = Column(Double, nullable=False)

    # Optional Fields
    description = Column(String, nullable=True)
    ingredients = Column(String, nullable=True)
    nutritional_info = Column(String, nullable=True)
    shelf_life = Column(String, nullable=True)

    # Enums
    category = Column(
        Enum(Category), nullable=False, server_default=Category.BASIC.value
    )
    sub_type = Column(
        Enum(SubCategory), nullable=True, server_default=SubCategory.BASIC.value
    )

    # Status and timestamps
    status = Column(String, nullable=True, server_default="1")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
