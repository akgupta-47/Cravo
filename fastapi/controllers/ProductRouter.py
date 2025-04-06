
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Product as ProductModel

''' <-
@Controller = Product Controller
@Description = All the API spec related to Product CRUD operations
@Tags = [Product]
-> '''
#-------------------------------
''' <-
@RouterBase = /products
-> '''
product_router = APIRouter(
    prefix='/products',
    tags=['Products']
)

''' <-
@Router = /all
@HttpMethod = GET
@Description = get all products that are active
@param = []
-> '''
product_router.get('/all')
async def getAllProducts(db: Session = Depends(get_db)):
    return await db.query(ProductModel)

''' <-
@Router = /all/category
@HttpMethod = GET
@Description = get all active products of particular category
@param = [category, string, category of the product]
-> '''
product_router.get('/all/category/{category}')
async def getAllProductsCategory(category: str, db: Session = Depends(get_db)):
    return await db.query(ProductModel).filter(ProductModel.category == category)

''' <-
@Router = /all/category
@HttpMethod = GET
@Description = get all active products of particular subcategory
@param = [category, string, category of the product]
@param = [subcategory, string, subcategory of the product]
-> '''
product_router.get('/all/category/{category}/{subcategory}')
async def getAllProductsSubCategory(category: str, subcategory: str, db: Session = Depends(get_db)):
    return await db.query(ProductModel).filter(ProductModel.category == category, ProductModel.sub_type == subcategory)