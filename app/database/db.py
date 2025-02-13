import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv, find_dotenv

env_path = find_dotenv()
load_dotenv(env_path)  # take environment variables from .env.
db_host = os.getenv("DB_HOST")  # Default to localhost if not set
engine = create_engine(
    f'postgresql://postgres:123123@{db_host}:5432/pizza_delivery', echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engine)


# Dependency to get a database session
def get_db():
    db = Session()  # Create a new session
    try:
        yield db  # Provide the session to the request
    finally:
        db.close()  # Ensure the session is closed after the request
