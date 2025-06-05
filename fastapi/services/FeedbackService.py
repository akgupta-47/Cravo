from typing import Optional

from data.FeedbackUpdateSchema import FeedbackUpdateSchema
from models.Feedback import Feedback as FeedbackModel
from models.ProductFeedback import ProductFeedback as ProductFeedbackModel
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from utils.AppError import AppError
from utils.DbExceptionHandler import handle_db_exceptions
from utils.DbUtils import clean_data


@handle_db_exceptions("Feedback Service")
async def commit_new_feedback(
    db: AsyncSession, feedback: FeedbackModel
) -> FeedbackModel:
    db.add(feedback)  # Stage the feedback for insertion
    await db.flush()  # Stage transaction
    await db.refresh(feedback)  # Refresh the instance to get DB-generated values
    return feedback  # Return the persisted feedback


@handle_db_exceptions("Feedback Service")
async def commit_new_product_feedback(db: AsyncSession, product_feedback: list):
    stmt = insert(ProductFeedbackModel).values(
        [
            {
                "product_id": p.product_id,
                "feedback_id": p.feedback_id,
                "rating_product": p.rating_product,
                "feedback_product": p.feedback_product,
            }
            for p in product_feedback
        ]
    )

    # Execute batch insert
    await db.execute(stmt)
    await db.flush()


@handle_db_exceptions("Feedback Service")
async def get_feedback_by_id(
    db: AsyncSession, feedback_id: str
) -> Optional[FeedbackModel]:
    """Fetch a single feedback by its ID."""
    stmt = select(FeedbackModel).filter(FeedbackModel.id == feedback_id)
    result = await db.execute(stmt)
    return result.scalars().first()  # Fetch the first matching feedback or None


async def get_product_feedback_by_id(db: AsyncSession, feedback_id: str):
    """Fetch feedback by its ID and return as a list."""
    stmt = select(ProductFeedbackModel).filter(
        ProductFeedbackModel.feedback_id == feedback_id
    )
    result = await db.execute(stmt)
    return result.scalars().all()  # Returns a list of matching feedback records


@handle_db_exceptions("Feedback Service")
async def update_feedback(
    db: AsyncSession, feedback_id: str, feedback_data: FeedbackUpdateSchema
):
    # Convert input schema to dict, excluding None values
    update_data = clean_data(feedback_data.model_dump(exclude_unset=True))

    # Extract product_feedback and remove it from update_data
    product_feedback_list = update_data.pop("product_feedback", None)

    # **Update FeedbackModel (excluding product_feedback)**
    stmt = (
        update(FeedbackModel)
        .where(FeedbackModel.id == feedback_id)
        .values(update_data)
        .returning(FeedbackModel)  # Returns the updated row
    )
    result = await db.execute(stmt)
    updated_feedback = result.fetchone()

    if not updated_feedback:
        raise AppError(
            status_code=404, component="Feedback Service", message="Feedback not found"
        )

    # **Handle Product Feedback Updates**
    if product_feedback_list is not None:
        existing_feedback = await db.execute(
            select(ProductFeedbackModel).where(
                ProductFeedbackModel.feedback_id == feedback_id
            )
        )

        existing_feedback = {p.product_id: p for p in existing_feedback.scalars().all()}

        for feedback in product_feedback_list:
            if feedback.get("product_id") in existing_feedback:
                # **Update existing feedback**
                stmt = (
                    update(ProductFeedbackModel)
                    .where(
                        ProductFeedbackModel.feedback_id == feedback_id,
                        ProductFeedbackModel.product_id == feedback.get("product_id"),
                    )
                    .values(
                        rating_product=feedback.get("rating"),
                        feedback_product=feedback.get("feedback"),
                    )
                )
                await db.execute(stmt)
            else:
                # **Insert new feedback (if ID is missing)**
                new_feedback = ProductFeedbackModel(
                    feedback_id=feedback_id,
                    product_id=feedback.get("product_id"),
                    rating_product=feedback.get("rating"),
                    feedback_product=feedback.get("feedback"),
                )
                db.add(new_feedback)

    await db.flush()
