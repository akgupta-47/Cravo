from fastapi import APIRouter

order_router = APIRouter(
    prefix='/orders',
    tags=['Orders']
)

@order_router.get('/')
def test_posts():
    return {"Hello": "World"}