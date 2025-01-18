from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

# Fetch the database URL from environment variables
SQLALCHEMY_DATABASE_URL = config("DATABASE_URL")

# Create the engine with pool_pre_ping enabled to manage stale connections
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# Define session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for models
Base = declarative_base()

# Dependency to handle database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
