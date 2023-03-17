
from pydantic import BaseModel, EmailStr
from typing import Optional

class Product(BaseModel):
    name:str
    price:float
    is_available:bool
    inventory:int

class UpdateProduct(BaseModel):
    price:float
    inventory:int

class Response_Model(BaseModel):
    name:str
    price:float

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    name:str
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    name:str
    email:EmailStr

    class Config:
        orm_mode = True

class Auth_Schema(BaseModel):
    email:EmailStr
    password:str

    class Config:
        orm_mode = True