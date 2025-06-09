import shortuuid
from data import ProductSchema
from database import ES, get_db
from logger import logger
from models.Product import Product as ProductModel
from services import ProductService as productService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from utils.AppError import AppError
from utils.ExceptionWrapper import handle_request

from fastapi import APIRouter, Depends, Query, Request

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


# product = {
#     "id": "p123",
#     "family_id": "f001",
#     "name": "Organic Almonds 500g",
#     "description": "Crunchy and healthy almonds",
#     "category": "food",
#     "sub_type": "basic",
#     "price": 399.0,
#     "weight": 0.5,
# }

# ES.index(index="products", id=product["id"], document=product)


@product_router.post("/new")
@handle_request
async def new_product(
    request: Request,
    product_data: ProductSchema.ProductBase,
    db: AsyncSession = Depends(get_db),
) -> ProductSchema.ProductBase:
    logger.info("Received new product creation request")

    # create the feedback id on the object
    product_data.id = shortuuid.uuid()

    if product_data.id is None:
        raise AppError(
            status_code=500,
            component="Product Service",
            message="product id creation failed",
        )

    new_product = ProductModel(**product_data.model_dump())

    new_es_product = ProductSchema.ProductESearch(
        id=product_data.id,
        family_id=product_data.family_id,
        image=product_data.image,
        name=product_data.name,
        description=product_data.description,
        unit=product_data.unit,
        price=product_data.price,
        weight=product_data.weight,
        category=product_data.category,
        sub_type=product_data.sub_type,
        status=product_data.status,
    )

    async with db.begin():
        logger.info("Committing product for product_id: %s", product_data.id)
        await productService.commit_new_product(db, new_product)
        logger.info(
            "Product committed successfully for product_id: %s", product_data.id
        )

    ES.index(index="products", id=product_data.id, document=new_es_product.model_dump())

    return new_product


@product_router.post("/one/{id}")
@handle_request
async def get_product(
    request: Request, id: str, db: AsyncSession = Depends(get_db)
) -> ProductSchema.ProductBase:

    product = await productService.get_product_by_id(db, id)

    if not product:
        logger.info("No product was found")
        raise AppError(
            status_code=404,
            component="Product Service",
            message="product with {id} not found",
        )

    return product


@product_router.post("/subcategory/{subcategory}")
@handle_request
async def get_product_by_category(
    request: Request, subcategory: str, db: AsyncSession = Depends(get_db)
) -> ProductSchema.ProductESearch:

    product = await productService.get_product_by_subcategory(db, subcategory)

    if not product:
        logger.info("No product for subcategory {subcategory} was found")
        raise AppError(
            status_code=404,
            component="Product Service",
            message="product with subcatgory {subcategory} not found",
        )

    return product


@product_router.get("/search")
@handle_request
async def search_products(
    request: Request, q: str = Query(..., min_length=1, max_length=50)
) -> list[ProductSchema.ProductESearch]:
    query = {
        "query": {
            "multi_match": {
                "query": q,
                "fields": ["name", "description", "catergory", "subcategory"],
            }
        }
    }
    res = ES.search(index="products", body=query)
    return [hit["_source"] for hit in res["hits"]["hits"]]


@product_router.put("/update/{id}")
@handle_request
def update_product(
    request: Request,
    id: str,
    update_product_fields: ProductSchema.ProductUpdate,
    db: AsyncSession = Depends(get_db),
) -> ProductSchema.ProductUpdate:

    updated_product = productService.update_product(id, update_product_fields, db)

    current_product = ProductSchema.ProductESearch(
        id=id,
        family_id=update_product_fields.family_id,
        image=update_product_fields.image,
        name=update_product_fields.name,
        description=update_product_fields.description,
        unit=update_product_fields.unit,
        price=update_product_fields.price,
        weight=update_product_fields.weight,
        category=update_product_fields.category,
        sub_type=update_product_fields.sub_type,
        status=update_product_fields.status,
    )

    ES.update(
        index="products",
        id=id,
        body={"doc": current_product.model_dump(exclude_none=True, exclude_unset=True)},
    )

    return updated_product


@handle_request
@product_router.get("/all")
async def getAllProducts(request: Request, db: Session = Depends(get_db)):
    return await db.query(ProductModel)


""" <-
@Router = /all/category
@HttpMethod = GET
@Description = get all active products of particular category
@param = [category, string, category of the product]
-> """
product_router.get("/all/category/{category}")
@handle_request
async def getAllProductsCategory(
    request: Request, category: str, db: Session = Depends(get_db)
):
    return await db.query(ProductModel).filter(ProductModel.category == category)


""" <-
@Router = /all/category
@HttpMethod = GET
@Description = get all active products of particular subcategory
@param = [category, string, category of the product]
@param = [subcategory, string, subcategory of the product]
-> """
product_router.get("/all/category/{category}/{subcategory}")
@handle_request
async def getAllProductsSubCategory(
    request: Request, category: str, subcategory: str, db: Session = Depends(get_db)
):
    return await db.query(ProductModel).filter(
        ProductModel.category == category, ProductModel.sub_type == subcategory
    )
