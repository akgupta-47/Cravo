from typing import Optional

from data import ProductSchema
from models.Product import Product as ProductModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from utils import AppError
from utils.DbExceptionHandler import handle_db_exceptions
from utils.DbUtils import clean_data


@handle_db_exceptions("Product Service")
async def commit_new_product(db: AsyncSession, product: ProductModel) -> ProductModel:
    db.add(product)  # Stage the product for insertion
    await db.flush()  # Stage transaction
    await db.refresh(product)  # Refresh the instance to get DB-generated values
    return product  # Return the persisted product


@handle_db_exceptions("Product Service")
async def get_product_by_id(
    db: AsyncSession, product_id: str
) -> Optional[ProductModel]:
    """Fetch a single product by its ID."""
    stmt = select(ProductModel).filter(ProductModel.id == product_id)
    result = await db.execute(stmt)
    return result.scalars().first()  # Fetch the first matching product or None


@handle_db_exceptions("Product Service")
async def get_product_by_subcategory(db: AsyncSession, subcategory: str):
    """Fetch a single product by its ID."""
    stmt = select(ProductModel).filter(ProductModel.sub_type == subcategory)
    result = await db.execute(stmt)
    return result.scalars().all()  # Fetch the first matching product or None


@handle_db_exceptions("Product Service")
async def update_product(
    product_id: str, updated_product: ProductSchema.ProductUpdate, db: AsyncSession
) -> ProductModel:

    # Convert input schema to dict, excluding None values
    update_data = clean_data(updated_product.model_dump(exclude_unset=True))

    # **Update FeedbackModel (excluding product_feedback)**
    stmt = (
        update(ProductModel)
        .where(ProductModel.id == product_id)
        .values(update_data)
        .returning(ProductModel)  # Returns the updated row
    )
    result = await db.execute(stmt)
    fetched_product = result.scalars().first()

    if not fetched_product:
        raise AppError(
            status_code=404, component="Product Service", message="Product not found"
        )

    return fetched_product
