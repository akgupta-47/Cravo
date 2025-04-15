import os

from database import get_db
from elasticsearch import Elasticsearch
from models import Product as ProductModel
from sqlalchemy.orm import Session
from utils.ExceptionWrapper import handle_request

from fastapi import APIRouter, Depends

""" <-
@Controller = Product Controller
@Description = All the API spec related to Product CRUD operations
@Tags = [Product]
-> """
# -------------------------------
""" <-
@RouterBase = /products
-> """
product_router = APIRouter(prefix="/products", tags=["Products"])

""" <-
@Router = /all
@HttpMethod = GET
@Description = get all products that are active
@param = []
-> """

es = Elasticsearch(os.getenv("POSTGRES_USER"))

product = {
    "id": "p123",
    "family_id": "f001",
    "name": "Organic Almonds 500g",
    "description": "Crunchy and healthy almonds",
    "category": "food",
    "sub_type": "basic",
    "price": 399.0,
    "weight": 0.5,
}

es.index(index="products", id=product["id"], document=product)


@handle_request
@product_router.get("/all")
async def getAllProducts(db: Session = Depends(get_db)):
    return await db.query(ProductModel)


""" <-
@Router = /all/category
@HttpMethod = GET
@Description = get all active products of particular category
@param = [category, string, category of the product]
-> """
product_router.get("/all/category/{category}")


async def getAllProductsCategory(category: str, db: Session = Depends(get_db)):
    return await db.query(ProductModel).filter(ProductModel.category == category)


""" <-
@Router = /all/category
@HttpMethod = GET
@Description = get all active products of particular subcategory
@param = [category, string, category of the product]
@param = [subcategory, string, subcategory of the product]
-> """
product_router.get("/all/category/{category}/{subcategory}")


async def getAllProductsSubCategory(
    category: str, subcategory: str, db: Session = Depends(get_db)
):
    return await db.query(ProductModel).filter(
        ProductModel.category == category, ProductModel.sub_type == subcategory
    )


@product_router.get("/search")
def search_products(q: str = Query(...)):
    resp = es.search(
        index="products",
        query={"multi_match": {"query": q, "fields": ["name", "description"]}},
    )
    return [hit["_source"] for hit in resp["hits"]["hits"]]
