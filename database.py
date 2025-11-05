from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connection URL (replace PASSWORD with your real postgres password)
DATABASE_URL = "postgresql://postgres:Mc%402323236@localhost:5432/taskdb"

# Create engine
engine = create_engine(DATABASE_URL)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
