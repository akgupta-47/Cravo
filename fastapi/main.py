from contextlib import asynccontextmanager
from typing import Union

import data.ItemSchema as item
from controllers.FeedbackRouter import feedback_router
from controllers.OrdersRouter import order_router
from controllers.ProductRouter import product_router
from controllers.TestRouter import test_router
from controllers.CartRouter import cart_router
from database import close_db, init_db
from dotenv import load_dotenv
from utils.AppError import AppError

from fastapi import FastAPI, HTTPException, Request, logger
from fastapi.responses import JSONResponse

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown lifecycle for the app."""
    print("Starting up...")  # Optional: Debug message
    await init_db()  # Initialize DB
    yield  # This allows the app to run
    print("Shutting down...")  # Optional: Debug message
    await close_db()  # Close DB connections


# Initialize FastAPI with lifespan
app = FastAPI(lifespan=lifespan)

app.include_router(order_router)
app.include_router(test_router)
app.include_router(feedback_router)
app.include_router(product_router)
app.include_router(cart_router)


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.to_dict()})


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    app_error = AppError.from_http_exception(exc, component="API Gateway")
    return JSONResponse(
        status_code=app_error.status_code, content={"error": app_error.to_dict()}
    )


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: item.Item):
    return {"item_name": item.name, "item_id": item_id}
