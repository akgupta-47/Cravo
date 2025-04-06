import shortuuid
from fastapi import APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from database import get_db
from models.Test import Test as TestModel
from logger import logger
from data.TestSchema import Test as TestSchema

test_router = APIRouter(
    prefix='/test',
    tags=['Test']
)

@test_router.post('/new')
async def create_new_test(test: TestSchema, db: AsyncSession = Depends(get_db)) -> TestSchema:
    new_test = TestModel(
        id=str(shortuuid.uuid()),  # Generate a unique ID
        title=test.title,
        content=test.content,
        published=test.published
    )

    try:
        db.add(new_test)  # Stage for insertion
        await db.commit()  # Commit transaction
        await db.refresh(new_test)  # Sync with DB to get generated values
        print("Transaction done successfully")
        return new_test  # Return after committing
    except Exception as e:
        await db.rollback()  # ❗ Rollback if there's an error
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
