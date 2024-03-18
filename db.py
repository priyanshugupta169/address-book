from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os


# Define the URL for your production database
SQLALCHEMY_DATABASE_URL = "sqlite:///./address_book.db"

# Define the URL for your test database
TEST_DATABASE_URL = "sqlite:///./test_address_book.db"

# Create an engine for the production database
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Create a SessionLocal class for the production database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create an engine for the test database
test_engine = create_engine(TEST_DATABASE_URL)
# Create a SessionLocal class for the test database
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Create a base class for your models
Base = declarative_base()

db = None
def get_db():
    global db
    if db is None:
        if os.environ.get("UNIT_TESTING") == "1":
            return TestSessionLocal()
        db = SessionLocal()
    return db



