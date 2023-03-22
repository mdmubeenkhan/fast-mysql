
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import Depends, HTTPException, status, APIRouter
from orm_dbconn.orm_db import get_db
from models import models
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from schema import schema
from auth import oauth2
import json


router = APIRouter(
    prefix="/product",
    tags=["Product"]
)

#skip is used by frontend for pagination
@router.get("/get-all/query-param")
def get_query_param(db:Session=Depends(get_db), user_detail:dict=Depends(oauth2.get_current_user), limit:int=5, skip=0, search: Optional[str]=""):
    data = db.query(models.Products).filter(models.Products.name.contains(search)).limit(limit).offset(skip).all()
    return data

#return all products of logged-in user
@router.get("/")
def get_all(db:Session=Depends(get_db), user_detail:dict=Depends(oauth2.get_current_user)):
    x, y = user_detail
    user_id = x[1]
    data = db.query(models.Products).filter(models.Products.user_id == int(user_id)).all()
    return {"data": data}


#Joining tables
@router.get("/get-products-list-added-by-all-user")
def get_products_list_added_by_user(db:Session=Depends(get_db), user_detail:dict=Depends(oauth2.get_current_user)):
    x, y = user_detail
    user_id = x[1]

    #bydefault sqlalchemy assumes join as left inner join
    # The output of below query will be list of tubles containing (Product object and user)
    data = db.query(models.Products, models.Users.name).join(models.Users, models.Products.user_id==models.Users.id).all()
    # print(str(data))
    # looping over list of tuples and fetching only product name and price from product object and adding user name to dict
    # we can fetch other information from product object like inventory, is_available
    # response_data = [{'name': product.name, 'price': product.price, 'added_by': user} for product, user in data]
    response_data = [{'name': product.name, 'price': product.price, 'availability':product.is_available, 'added_by': user} for product, user in data]

    # response = json.dumps(data, cls=schema.Product_Name_Price_Resp)
    #data = db.query(models.Products.name, models.Products.price, models.Users.name).join(models.Users, models.Products.user_id==models.Users.id).all()
    
    # converting list of tuples into list of dictionary using dictionary comprehension
    #response = [{"name": d[0], "price": d[1], "user": d[2]} for d in data]

    return response_data

#Joining and GROUP BY
@router.get("/no-of-product-added-by-user", response_model=List[schema.NoOfProductAddedByUser])
def get_no_of_product_added_by_user(db:Session=Depends(get_db), user_detail:dict=Depends(oauth2.get_current_user)):
    
    data = db.query(models.Users, func.count(models.Products.id).label("NoOfProductAddedByUser")).join(models.Products, models.Products.user_id==models.Users.id).group_by(models.Users.name).all()
    print(str(data))
    # response_data = [{'name': users.name,  'count': count} for users, count in data]

    return data

#Joining and Filter
@router.get("/list-of-product-by-logged-in-user", response_model=List[schema.ProductResponse_Model])
def get_product_list_by_logged_in_user(db:Session=Depends(get_db), user_detail:dict=Depends(oauth2.get_current_user)):
    x, y = user_detail
    logged_in_user_id = x[1]
    data = db.query(models.Products).join(models.Users, models.Products.user_id==models.Users.id).filter(models.Users.id==logged_in_user_id).all()
    print(str(data))
    # response_data = [{'name': users.name,  'count': count} for users, count in data]

    return data



#return all products of ALL USERS with limited field information
#Response model added, to send only few fields to user
@router.get("/resp", status_code=status.HTTP_200_OK, response_model=List[schema.Response_Model])
def get_all_limited_field(db:Session=Depends(get_db), user_detail:dict=Depends(oauth2.get_current_user)):
    data = db.query(models.Products).all()
    return data

#Response model added, to send only few fields to user
#jsonable_encoder converts model data type to json data type
@router.get("/resp/{id}", status_code=status.HTTP_200_OK, response_model=schema.Response_Model)
def get_specific_product(id:int, db:Session=Depends(get_db), user_detail:dict=Depends(oauth2.get_current_user)):
    data = db.query(models.Products).filter(models.Products.id==id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id = {id} not found.")

    a, b = user_detail
    user_id = a[1]

    if user_id != str(data.user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Others product details cant be seen.")
        
    return data

@router.get("/{id}")
def get_specific_product_without_login(id:int, db:Session=Depends(get_db)):
    data = db.query(models.Products).filter(models.Products.id==id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id = {id} not found.")
    return {"data": data}

@router.post("/old-way")
def add_new_product_old(payload:schema.Product, db:Session=Depends(get_db)):
    new_product = models.Products(name=payload.name, price=payload.price, is_available=payload.is_available, inventory=payload.inventory)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"data": new_product}

# even if we pass extra key value data in the post request, Schema will ignore
# **payload.dict() this unpacks the body data like dictionary
@router.post("/")
def add_new_product(payload:schema.Product, db:Session=Depends(get_db), user_detail:dict=Depends(oauth2.get_current_user)):
    a, b = user_detail
    user_id = a[1]
    new_dict = payload.dict()
    new_dict.update({"user_id": user_id})
    # new_product = models.Products(**payload.dict())
    new_product = models.Products(**new_dict)
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"data": new_product}

@router.delete("/{id}")
def delete_product(id:int, db:Session=Depends(get_db), user_detail:dict=Depends(oauth2.get_current_user)):
    data = db.query(models.Products).filter(models.Products.id==id)
    if not data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id = {id} not found.")
    
    a, b = user_detail
    user_id = a[1]

    if user_id != str(data.first().user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You cannot delete others product.")
    
    data.delete(synchronize_session=False)
    db.commit()
    return {"details":f"Record with id = {id} is deleted."}


@router.put("/{id}")
def update(id:int, payload:schema.Product, db:Session=Depends(get_db), user_detail:dict=Depends(oauth2.get_current_user)):
    data = db.query(models.Products).filter(models.Products.id==id)
    if not data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id = {id} not found.")

    a, b = user_detail
    user_id = a[1]

    if user_id != str(data.first().user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You cannot edit others product.")

    data.update(payload.dict(), synchronize_session=False)
    db.commit()
    return {"data": data.first()}