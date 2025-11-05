from sqlalchemy import Column, Integer, String, Boolean
from database import Base, engine

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

# Create table
Base.metadata.create_all(bind=engine)
