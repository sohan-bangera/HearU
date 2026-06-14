from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()

# Read DATABASE URL from .env file
# THis is your Supabase PostgreSQL connection string
DATABASE_URL = os.getenv("DATABASE_URL")

# create_engine opens a connection pool to postgreSQL
# echo=True prints every SQL query to terminal (helpful for learning/debugging)
# Turn echo=False in production
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    # Looks at all SQLModel models and creates their tables in PostgreSQL
    # Safe to call every startup - skips tables that already exist
    SQLModel.metadata.create_all(engine)

def get_session():
    # A generator function that gives routes a database session
    # "with" ensures the session is always closed after use, even if an error occurs
    with Session(engine) as session:
        yield session