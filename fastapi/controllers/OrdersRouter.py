from datetime import date
import shortuuid
from fastapi import APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from database import get_db
from controllers import TrackRouter
from models import OrderProductMapper as OrderProductMapperModel
from models.Order import Order as OrderModel
from models.Feedback import Feedback as FeedbackModel
import services.OrderService as orderService
import services.TrackService as trackService
from logger import logger
from data.OrderSchema import Order as OrderSchema

""" <-
@Controller = Order Controller
@Description = All the API spec related to Orders CRUD operations
@Tags = [Order]
-> """
# --------------------
""" <-
@RouterBase = /orders
-> """
order_router = APIRouter(prefix="/orders", tags=["Orders"])


def getLoggedInUser():
    loggedin_user = {}
    loggedin_user["user_id"] = "abcd"
    return loggedin_user


def getLoggedInUserShopId():
    # loggedin_user = {}
    # loggedin_user["user_id"] = "abcd"
    return "abcd"


@order_router.get("/")
def test_posts():
    return {"Order": "Order Routes are active!!"}


""" <-
@Router = /all/user
@HttpMethod = GET
@Description = get all the orders placed by a certain user
@param = []
-> """


@order_router.get("/all/user")
async def get_all_orders_by_user(db: Session = Depends(get_db)):
    loggedin_user = getLoggedInUser()
    result = await orderService.get_all_orders_by_user(db, loggedin_user["user_id"])
    if not result:
        logger.info("No order was found")
        raise HTTPException(status_code=404, detail="orders not found")
    return result


""" <-
@Router = /all/shop
@HttpMethod = GET
@Description = get all the orders that are fullfilled by a certain shop
@param = []
-> """


@order_router.get("/all/shop")
async def get_all_orders_by_shop(db: Session = Depends(get_db)):
    shop_id = getLoggedInUserShopId()
    result = await orderService.get_all_orders_by_shop(db, shop_id)
    if not result:
        logger.info("No order was found")
        raise HTTPException(status_code=404, detail="orders not found")
    return result


""" <-
@Router = /{order_id}
@HttpMethod = GET
@Description = get a particular order with a certain order id
@param = [order_id,string,order id of the order]
-> """


@order_router.get("/{id}")
async def get_order_by_id(id: str, db: Session = Depends(get_db)) -> dict:
    result = await orderService.get_order_by_id(db, id)
    if not result:
        logger.info("No order was found")
        raise HTTPException(status_code=404, detail="order with {id} not found")
    return result


""" <-
@Router = /new 
@HttpMethod = POST
@Description = create new order 
@param = [order_object,model,fields that are required to store a new order]
-> """


@order_router.post("/new")
async def create_new_order(
    order: OrderSchema, db: Session = Depends(get_db)
) -> OrderSchema:
    loggedin_user = getLoggedInUser()
    order.user_id = loggedin_user["user_id"]

    # create new order object and commit in the database
    new_order = OrderModel(
        id=str(shortuuid.uuid()),
        total=order.total,
        track_id=order.track_id,
        user_id=loggedin_user["user_id"],
        shop_id=order.shop_id,
        address_id=order.address_id,
        bid_id=order.bid_id,
        payment_id=order.payment_id,
    )

    new_track = TrackRouter.createNewTrack(new_order, db)
    new_order.track_id = new_track.id

    await orderService.commit_new_order(db, new_order)
    await trackService.commit_new_track(db, new_track)

    # iterate over the product list and add product order mapping
    product_orders = [
        OrderProductMapperModel(
            product_id=product.id,
            order_id=new_order.id,
            quantity=product.quantity,
            available=True,
        )
        for product in order.products
    ]

    # Batch insert for efficiency
    await orderService.commit_new_op_mappers(db, product_orders)

    return new_order


""" <-
@Router = /update/feedback
@HttpMethod = PATCH
@Description = take user feedback and update rating & feedback for shop and products
@param = [order_object,model,fields that are required to update feedback for the order]
-> """


# feedback for every item, shop and delivery
@order_router.patch("/update/feedback")
async def update_order_rating(
    order: OrderSchema, db: AsyncSession = Depends(get_db)
) -> OrderSchema:
    loggedin_user = getLoggedInUser()
    # Fetch the order
    order_item = await orderService.get_order_by_id(db, order.id)

    if not order_item:
        logger.info(f"No order found with id: {order.id}")
        raise HTTPException(
            status_code=404, detail=f"Order with id: {order.id} not found"
        )

    # Handle feedback creation if provided
    if order.feedback:
        # If feedback doesn't exist, create a new one
        new_feedback = FeedbackModel(
            id=str(shortuuid.uuid()),  # Generate a new UUID
            feedback=order.feedback,
            user_id=loggedin_user["user_id"],
            shop_id=order.shop_id,
            order_id=order.id,
        )
        try:
            db.add(new_feedback)
            await db.commit()  # Commit feedback to DB
            await db.refresh(new_feedback)  # Refresh to get the inserted object
        except Exception as e:
            await db.rollback()  # Rollback in case of an error
            logger.error(f"Error creating feedback: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to create feedback")

    # Update order rating
    order_item.rating = order.rating
    try:
        await db.commit()  # Commit the order rating update to DB
        await db.refresh(order_item)  # Refresh the updated order
    except Exception as e:
        await db.rollback()  # Rollback in case of an error
        logger.error(f"Error updating order rating: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update order rating")

    return order_item  # Return the updated order item


""" <-
@Router = /update/arrival_time
@HttpMethod = PATCH
@Description = update the time when order got delivered
@param = [order_object,model,fields that are required to update the delivered timing of new order]
-> """


@order_router.patch("/update/arrival_time")
async def update_order_arrival_time(order: OrderSchema, db: Session = Depends(get_db)):
    order_item = await orderService.get_order_by_id(db, order.id)

    if not order_item:
        logger.info("No order was found")
        raise HTTPException(
            status_code=404, detail=f"order with id: {order.id} not found"
        )

    order_item.arrived_at = date.now()
    db.commit()


""" <-
@Router = /update/unavailable/item
@HttpMethod = PATCH
@Description = update the items that are unavailable, handle the case id partial amount of items are unavailable, start refund process
@param = [order_object,model,fields that are required to track items that are unavailable after placing a new order]
-> """


# complete this
@order_router.patch("/update/unavailable/item")
async def update_unavailable_item(order: OrderSchema, db: Session = Depends(get_db)):
    unavailable_products = order.products

    for product in unavailable_products:
        product_item = await orderService.get_order_product_mapping(
            db, product.id, order.id
        )

        if not product_item:
            logger.info("No product-order mapping was found")
            raise HTTPException(
                status_code=404,
                detail=f"order-product mapping with product id: {product_item.product_id} & order id: {order.id} not found",
            )

        if product.quantity == product_item.quantity:
            product_item.available = False
            db.commit()
        else:
            new_count = product_item.quantity - product.quantity
            new_product_order = product_item
            new_product_order.quantity = new_count
            db.commit()

            await orderService.delete_op_mapping(
                db, product.id, order.id, product_item.quantity
            )
            # add services to start a refund process
