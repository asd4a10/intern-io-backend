from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Step 1: Create a PostgreSQL engine
DATABASE_URL = "postgresql://leveroff:@localhost/internio"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Step 2: Define a base class
Base = declarative_base()


# Step 3: Define a model (which corresponds to a table in the database)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    google_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    link = Column(String)
    img = Column(String)
    category = Column(String)
    description = Column(String)


# Step 4: Create the table in the database (if it doesn't exist)
Base.metadata.create_all(bind=engine)


# Dependency for database session management
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
