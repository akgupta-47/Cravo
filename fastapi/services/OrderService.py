from typing import List
import shortuuid
from sqlalchemy import delete
from sqlalchemy.orm import Session
from data import OrderSchema
from models import OrderProductMapper as OrderProductMapperModel
from models.Order import Order as OrderModel

def get_all_orders_by_user(db: Session, loggedin_user: str) -> List[OrderModel]:
    return db.query(OrderModel).filter(OrderModel.user_id == loggedin_user)

def get_all_orders_by_shop(db: Session, shop_id: str) -> List[OrderModel]:
    return db.query(OrderModel).filter(OrderModel.shop_id == shop_id)

def get_order_by_id(db: Session, order_id: str) -> OrderModel:
    return db.query(OrderModel).filter(OrderModel.id == order_id)

def commit_new_order(db: Session, new_order: OrderModel):
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

def commit_new_op_mapper(db: Session, new_op_mapping: OrderProductMapperModel):
    db.add(new_op_mapping)
    db.commit()
    db.refresh(new_op_mapping)
    
def get_order_product_mapping(db: Session, product_id: str, order_id: str) -> OrderProductMapperModel:
    return db.query(OrderProductMapperModel).filter(OrderProductMapperModel.product_id == product_id, OrderProductMapperModel.order_id == order_id).first()

def delete_op_mapping(db: Session, product_id: str, order_id: str, quantity: int):
    delete_query = delete(OrderProductMapperModel).where(OrderProductMapperModel.product_id == product_id, OrderProductMapperModel.order_id == order_id, OrderProductMapperModel.quantity == quantity)
    db.execute(delete_query)