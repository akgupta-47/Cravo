import shortuuid
from data.FeedbackSchema import FeedbackSchema
from data.FeedbackUpdateSchema import FeedbackUpdateSchema
from database import get_db
from logger import logger
from models.Feedback import Feedback as FeedbackModel
from models.ProductFeedback import ProductFeedback as ProductFeedbackModel
from services import FeedbackService as feedbackService
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from utils.AppError import AppError
from utils.ExceptionWrapper import handle_request

from fastapi import APIRouter, Depends, HTTPException

feedback_router = APIRouter(prefix="/feedback", tags=["Feedback"])


def prepareFeedbackSchema(
    feedback: FeedbackModel, pf: list[ProductFeedbackModel]
) -> FeedbackSchema:
    feedback_dict = (
        feedback.model_dump() if hasattr(feedback, "model_dump") else feedback.__dict__
    )

    product_feedback_list = [
        {
            "id": p.product_id,  # Ensure correct mapping of field names
            "rating": p.rating_product,
            "feedback": p.feedback_product,
        }
        for p in pf
    ]

    return FeedbackSchema(**feedback_dict, product_feedback=product_feedback_list)


@feedback_router.post("/new")
@handle_request
async def new_order_feedback(
    feedback: FeedbackSchema, db: AsyncSession = Depends(get_db)
) -> FeedbackSchema:
    logger.info("Received new feedback request for order_id: %s", feedback.order_id)

    # create the feedback id on the object
    feedback.id = shortuuid.uuid()

    new_feedback = FeedbackModel(
        id=feedback.id,
        rating_order=feedback.rating_order,
        feedback_order=feedback.feedback_order,
        rating_shop=feedback.rating_shop,
        feedback_shop=feedback.feedback_shop,
        rating_delivery=feedback.rating_delivery,
        feedback_delivery=feedback.feedback_delivery,
        shop_id=feedback.shop_id,
        order_id=feedback.order_id,
        agent_id=feedback.agent_id,
    )

    new_product_feedback = [
        ProductFeedbackModel(
            feedback_id=new_feedback.id,
            product_id=product.id,
            rating_product=product.rating,
            feedback_product=product.feedback,
        )
        for product in feedback.product_feedback
    ]

    async with db.begin():
        logger.info("Committing feedback for order_id: %s", feedback.order_id)
        await feedbackService.commit_new_feedback(db, new_feedback)
        logger.info(
            "Feedback committed successfully for order_id: %s", feedback.order_id
        )

        logger.info(
            "Committing product feedback entries for order_id: %s", feedback.order_id
        )
        await feedbackService.commit_new_product_feedback(db, new_product_feedback)
        logger.info(
            "Product feedback committed successfully for order_id: %s",
            feedback.order_id,
        )

    feedback.product_feedback = [
        {
            "id": product.product_id,
            "rating": product.rating_product,
            "feedback": product.feedback_product,
        }
        for product in new_product_feedback
    ]

    return feedback


@feedback_router.get("/{id}")
@handle_request
async def get_feedback_for_order(
    id: str, db: AsyncSession = Depends(get_db)
) -> FeedbackSchema:

    feedback = await feedbackService.get_feedback_by_id(db, id)

    if not feedback:
        logger.info("No feedback was found")
        raise AppError(
            status_code=404,
            component="Feedback Service",
            message="feedback with {id} not found",
        )

    product_feedback = await feedbackService.get_product_feedback_by_id(db, id)

    if not product_feedback:
        logger.info("No product feedback was found")
        raise AppError(
            status_code=404,
            component="Feedback Service",
            message="feedback for products not found",
        )

    return prepareFeedbackSchema(feedback, product_feedback)


# instead of using single ones lets just give the list only
@feedback_router.get("/order/{id}")
async def get_feedback_for_order(
    id: str, db: AsyncSession = Depends(get_db)
) -> FeedbackSchema:

    feedback = await feedbackService.get_shop_feedback_by_id(db, id)

    if not feedback:
        logger.info("No feedback was found")
        raise HTTPException(status_code=404, detail="feedback with {id} not found")

    fdbk = FeedbackSchema(
        id=feedback.id,
        rating_shop=feedback.rating_shop,
        feedback_shop=feedback.feedack_shop,
        shop_id=feedback.shop_id,
    )

    return fdbk


@feedback_router.put("/{feedback_id}")
@handle_request
async def update_feedback_route(
    feedback_id: str,
    feedback_data: FeedbackUpdateSchema,
    db: AsyncSession = Depends(get_db),
):

    updated_feedback = await feedbackService.update_feedback(
        db, feedback_id, feedback_data
    )
    return updated_feedback
