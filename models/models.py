from orm_dbconn.orm_db import Base
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func

class Products(Base):
    __tablename__ = "Products"

    id = Column(Integer, primary_key=True)
    name = Column(String(15), nullable=False)
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, nullable=True, server_default="0")
    inventory = Column(Integer, nullable=True, server_default="0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

