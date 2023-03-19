from orm_dbconn.orm_db import Base
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func

class Products(Base):
    __tablename__ = "Products"

    id = Column(Integer, primary_key=True)
    name = Column(String(15), nullable=False)
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, nullable=True, server_default="0")
    inventory = Column(Integer, nullable=True, server_default="0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    #Below for Foreign key, User refers to Table name, not the class name
    #Both class name and Table name is same in our case, but we should remember to use only Tablename
    user_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    name = Column(String(15), nullable=False)
    email = Column(String(25), nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())