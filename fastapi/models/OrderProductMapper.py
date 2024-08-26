from sqlmodel import SQLModel, Field
from datetime import datetime

class OrderProductMapperBase(SQLModel):
    order_id: str
    product_id: str
    quantity: int
    created_at: datetime = Field(default=datetime.UTC)

class OrderProductMapper(OrderProductMapperBase, table=True):
    id = str = Field(default=None, primary_key=True)