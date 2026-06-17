import os                               # Importing the os module to interact with the operating system, particularly for accessing environment variables
from sqlalchemy import create_engine    # Importing the create_engine function from SQLAlchemy to create a database engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase  # Importing necessary components from SQLAlchemy for creating a database engine and session
from dotenv import load_dotenv          # Importing the load_dotenv function from the python-dotenv package to load environment variables from a .env file

load_dotenv() # Load environment variables from a .env file, allowing the application to access database credentials and other configuration settings without hardcoding them in the code

POSTGRES_USER = os.getenv('POSTGRES_USER')  
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT',"5432")

# Database connection settings, constructed using environment variables for security and flexibility
DB_URL = (f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

engine = create_engine(DB_URL, pool_pre_ping=True) # Create POSTGRES_DBg the database URL constructed from environment variables, which allows the application to connect to the PostgreSQL database
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False) # Create a session factory using SQLAlchemy's sessionmaker, which will be used to create database sessions for interacting with the database

# Base class for all database models, using SQLAlchemy's DeclarativeBase
class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()

    try:
        yield db # Yield the database session to be used in the application, allowing for proper management of database connections
    finally:
        db.close() # Ensure the database session is closed after use
