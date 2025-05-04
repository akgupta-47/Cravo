import os

from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load environment variables
load_dotenv()

# Ensure all required environment variables are set
required_env_vars = [
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_HOST",
    "POSTGRES_PORT",
    "POSTGRES_DB",
]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(
        f"🚨 Missing required environment variables: {', '.join(missing_vars)}"
    )

# Get PostgreSQL credentials
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
url = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
db = os.getenv("POSTGRES_DB")

# Use `asyncpg` as async driver
POSTGRES_DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{url}:{port}/{db}"

# Create an async engine
async_engine = create_async_engine(POSTGRES_DATABASE_URL, echo=True, future=True)

# Create a base class for models
Base = declarative_base()

# Create an async session factory
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Keeps session open after commits
)


async def init_db():
    """Create tables asynchronously"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Database session dependency for FastAPI
async def get_db():
    """Dependency to get DB session with error handling"""
    async with AsyncSessionLocal() as db:
        try:
            yield db  # Yield the session to FastAPI routes
            await db.commit()  # Commit changes if no errors
        except Exception as e:
            await db.rollback()  # 🚨 Rollback on error
            raise e  # Re-raise exception for handling
        finally:
            await db.close()  # Ensure session is closed


async def close_db():
    """Ensure engine is properly disposed when app shuts down"""
    await async_engine.dispose()


ES = Elasticsearch(os.getenv("ELASTIC_SEARCH_SERVER"))
