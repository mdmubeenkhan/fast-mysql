
from pydantic import BaseModel, EmailStr
from typing import Optional

class Product(BaseModel):
    name:str
    price:float
    is_available:bool
    inventory:int

class ProductCreate(Product):
    user_id:int

class UpdateProduct(BaseModel):
    price:float
    inventory:int


class UserResponse(BaseModel):
    name:str
    email:EmailStr

    class Config:
        orm_mode = True


class Response_Model(BaseModel):
    name:str
    price:float
    owner: UserResponse
    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    name:str
    email:EmailStr
    password:str


class AuthSchema(BaseModel):
    email:EmailStr
    password:str

    class Config:
        orm_mode = True

class AuthToken(BaseModel):
    access_token:str
    token_type:str
    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id:str
    role:str

class Purchase(BaseModel):
    product_id:int
    quantity:int

class Product_Name_Price_Resp(BaseModel):
    name:str
    price:float
    class Config:
        orm_mode = True

class PurchaseResponse(BaseModel):
    product_id:int
    quantity:int
    owner: UserResponse
    product: Product_Name_Price_Resp
    class Config:
        orm_mode = True

class UserNameResponse(BaseModel):
    name:str
    class Config:
        orm_mode = True

class ProductResponse_Model(BaseModel):
    name:str
    price:float
    is_available:bool
    inventory:int
    owner: UserResponse
    class Config:
        orm_mode = True

class NoOfProductAddedByLoggedInUser(BaseModel):
    # Users: UserNameResponse
    Products: ProductResponse_Model
    class Config:
        orm_mode = True


# Name of the Key in this schema should match with the names in the response of data coming in api post query execution
# data = db.query(models.Users, func.count(models.Products.id).label("NoOfProductAddedByUser")).join(models.Products, models.Products.user_id==models.Users.id).group_by(models.Users.name).all()
# label =    NoOfProductAddedByUser should match in schema NoOfProductAddedByUser: int
# models.Users should match in schema = Users: UserResponse
class NoOfProductAddedByUser(BaseModel):
    Name: UserResponse
    NoOfProductAddedByUser: int
    class Config:
        orm_mode = True