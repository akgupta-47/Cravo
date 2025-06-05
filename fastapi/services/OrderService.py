from typing import List, Optional
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from models.OrderProductMapper import OrderProductMapper as OrderProductMapperModel
from models.Order import Order as OrderModel

async def get_all_orders_by_user(db: AsyncSession, loggedin_user: str) -> List[OrderModel]:
    """Fetch all orders for a specific user."""
    stmt = select(OrderModel).filter(OrderModel.user_id == loggedin_user)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_all_orders_by_shop(db: AsyncSession, shop_id: str) -> List[OrderModel]:
    """Fetch all orders for a specific shop."""
    stmt = select(OrderModel).filter(OrderModel.shop_id == shop_id)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_order_by_id(db: AsyncSession, order_id: str) -> Optional[OrderModel]:
    """Fetch a single order by its ID."""
    stmt = select(OrderModel).filter(OrderModel.id == order_id)
    result = await db.execute(stmt)
    return result.scalars().first()  # Fetch the first matching order or None

async def commit_new_order(db: AsyncSession, new_order: OrderModel) -> OrderModel:
        try:
            db.add(new_order)  # Stage the order for insertion
            await db.commit()  # Commit transaction
            await db.refresh(new_order)  # Refresh the instance to get DB-generated values
            return new_order  # Return the persisted order
        except Exception as e:
            await db.rollback()  # Rollback in case of an error
            raise e
    
async def commit_new_op_mappers(db: AsyncSession, product_orders: list):
    try:
        # Use bulk insert with `insert()` for best performance
        stmt = insert(OrderProductMapperModel).values([{
            "product_id": p.product_id,
            "order_id": p.order_id,
            "quantity": p.quantity,
            "available": p.available
        } for p in product_orders])

        # Execute batch insert
        await db.execute(stmt)
        await db.commit()

    except Exception as e:
        await db.rollback()
        raise e
    
async def get_order_product_mapping(db: AsyncSession, product_id: str, order_id: str) -> Optional[OrderProductMapperModel]:
    stmt = select(OrderProductMapperModel).filter(OrderProductMapperModel.product_id == product_id, OrderProductMapperModel.order_id == order_id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def delete_op_mapping(db: AsyncSession, product_id: str, order_id: str, quantity: int) -> None:
    """Delete a product-order mapping."""
    stmt = (
        delete(OrderProductMapperModel)
        .where(
            OrderProductMapperModel.product_id == product_id,
            OrderProductMapperModel.order_id == order_id,
            OrderProductMapperModel.quantity == quantity
        )
    )
    
    await db.execute(stmt)  # Execute the delete statement
    await db.commit()  # Commit changes