import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Use DATABASE_URL if set, otherwise fallback to manual config
db_url = os.getenv("DATABASE_URL")
if not db_url:
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Create engine and session
engine = create_engine(db_url, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Dependency to get a database session


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
