from datetime import datetime
from fastapi import APIRouter, Request
from utils.ExceptionWrapper import handle_request
from utils.AppError import AppError

from proto.protobuf.cart_pb2 import Cart
from data.CartSchema import Cart as CartSchema
from database import redis_client

# Define FastAPI router
cart_router = APIRouter(prefix="/cart", tags=["Cart"])


@cart_router.post("/add-to-cart")
@handle_request
async def save_cart(request: Request, cart: CartSchema):

    current_time = datetime.utcnow()  # Get the current UTC time in ISO 8601 format
    cart.created_at = (
        cart.created_at or current_time
    )  # Set `created_at` if not already provided
    cart.updated_at = current_time
    # Check if a cart already exists for the user
    existing_cart_data = redis_client.get(cart.user_id)
    # if existing_cart_data is None:
    #     raise AppError(
    #         status_code=404,
    #         component="Cart Service",
    #         message=f"Cart for user_id {cart.user_id} not found",
    #     )
    cart_proto = Cart()

    if existing_cart_data:
        # Deserialize existing cart data
        cart_proto.ParseFromString(existing_cart_data)

        # Update quantities, add new items, or delete items
        existing_items = {item.product_id: item for item in cart_proto.items}
        for item in cart.items:
            if item.product_id in existing_items:
                if item.quantity == 0:
                    # Remove item if quantity is 0
                    del existing_items[item.product_id]
                else:
                    # Update item quantity
                    existing_items[item.product_id].quantity = item.quantity
                    existing_items[item.product_id].product_name = item.product_name
                    existing_items[item.product_id].price = item.price
            else:
                if item.quantity > 0:
                    # Add new item if quantity is greater than 0
                    new_item = cart_proto.items.add()
                    new_item.product_id = item.product_id
                    new_item.product_name = item.product_name
                    new_item.quantity = item.quantity
                    new_item.price = item.price

        # Rebuild the cart_proto items list
        cart_proto.items.clear()
        for item in existing_items.values():
            cart_proto.items.add().CopyFrom(item)

        # Update fee details
        cart_proto.fee.total = cart.fee.total
        cart_proto.fee.platform_fee = cart.fee.platform_fee
        cart_proto.fee.surge = cart.fee.surge
        cart_proto.fee.delivery = cart.fee.delivery
        cart_proto.fee.tax = cart.fee.tax
        cart_proto.fee.discount = cart.fee.discount
        cart_proto.fee.final = cart.fee.final

        # Update other cart fields
        cart_proto.coupon = cart.coupon
        cart_proto.status = cart.status
        cart_proto.updated_at = cart.updated_at.isoformat()
    else:
        # Create a new cart if none exists
        cart_proto.user_id = cart.user_id
        for item in cart.items:
            if item.quantity > 0:  # Only add items with quantity > 0
                item_proto = cart_proto.items.add()
                item_proto.product_id = item.product_id
                item_proto.product_name = item.product_name
                item_proto.quantity = item.quantity
                item_proto.price = item.price

        # Set fee details
        cart_proto.fee.total = cart.fee.total
        cart_proto.fee.platform_fee = cart.fee.platform_fee
        cart_proto.fee.surge = cart.fee.surge
        cart_proto.fee.delivery = cart.fee.delivery
        cart_proto.fee.tax = cart.fee.tax
        cart_proto.fee.discount = cart.fee.discount
        cart_proto.fee.final = cart.fee.final

        # Set other cart fields
        cart_proto.coupon = cart.coupon
        cart_proto.status = cart.status
        cart_proto.created_at = cart.created_at.isoformat()
        cart_proto.updated_at = cart.updated_at.isoformat()

    print(cart_proto)

    # Store updated serialized data in Redis
    if not redis_client.set(cart.user_id, cart_proto.SerializeToString()):
        raise AppError(
            status_code=500,
            component="Cart Service",
            message="Failed to save cart data to Redis",
        )
    return {"message": "Cart updated successfully"}


@cart_router.get("/{user_id}")
@handle_request
async def get_cart(request: Request, user_id: str) -> CartSchema:
    # Retrieve serialized data from Redis
    cart_data = redis_client.get(user_id)
    if not cart_data:
        raise AppError(
            status_code=404,
            component="Cart Service",
            message=f"Cart for user_id {user_id} not found",
        )

    if isinstance(cart_data, str):
        cart_data = cart_data.encode("utf-8")

    # Deserialize data using protobuf
    cart_proto = Cart()
    cart_proto.ParseFromString(cart_data)

    # Convert protobuf object to dictionary
    cart_dict = {
        "user_id": cart_proto.user_id,
        "items": [
            {
                "product_id": item.product_id,
                "product_name": item.product_name,
                "quantity": item.quantity,
                "price": item.price,
            }
            for item in cart_proto.items
        ],
        "fee": {
            "total": cart_proto.fee.total,
            "platform_fee": cart_proto.fee.platform_fee,
            "surge": cart_proto.fee.surge,
            "delivery": cart_proto.fee.delivery,
            "tax": cart_proto.fee.tax,
            "discount": cart_proto.fee.discount,
            "final": cart_proto.fee.final,
        },
        "coupon": cart_proto.coupon,
        "status": cart_proto.status,
        "created_at": (
            datetime.fromisoformat(cart_proto.created_at)
            if cart_proto.created_at
            else None
        ),
        "updated_at": (
            datetime.fromisoformat(cart_proto.updated_at)
            if cart_proto.updated_at
            else None
        ),
    }

    cart_schema = CartSchema.model_validate(cart_dict)
    return cart_schema
