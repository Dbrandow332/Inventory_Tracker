from sqlalchemy import Column, Integer, String
from app.database import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    count = Column(Integer, default=0)