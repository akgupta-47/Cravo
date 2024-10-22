from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

user = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PASSWORD")
url = os.environ.get("POSTGRES_HOST")
port = str(os.environ.get("POSTGRES_PORT"))
db = os.environ.get("POSTGRES_DB")

# SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:pgsql3214@localhost:5432/cravo'
SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{url}:{port}/{db}?sslmode=require"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
