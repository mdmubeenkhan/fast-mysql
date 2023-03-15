
from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    name:str
    price:float
    is_available:bool
    inventory:int

class UpdateProduct(BaseModel):
    price:float
    inventory:int
