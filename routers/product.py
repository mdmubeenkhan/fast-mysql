
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from orm_dbconn.orm_db import get_db
from models import models
from fastapi.encoders import jsonable_encoder
from typing import List
from schema import schema
from auth import oauth2


router = APIRouter(
    prefix="/product",
    tags=["Product"]
)

#skip is used by frontend for pagination
@router.get("/get-all/query-param")
def get_all(db:Session=Depends(get_db), user_detail:dict=Depends(oauth2.get_current_user), limit:int=5, skip=0):
    print(limit)
    data = db.query(models.Products).limit(limit).offset(skip).all()
    return data

#return all products of logged-in user
@router.get("/")
def get_all(db:Session=Depends(get_db), user_detail:dict=Depends(oauth2.get_current_user)):
    x, y = user_detail
    user_id = x[1]
    data = db.query(models.Products).filter(models.Products.user_id == int(user_id)).all()
    return {"data": data}

#return all products of ALL USERS with limited field information
#Response model added, to send only few fields to user
@router.get("/resp", status_code=status.HTTP_200_OK, response_model=List[schema.Response_Model])
def get_all(db:Session=Depends(get_db), user_detail:dict=Depends(oauth2.get_current_user)):
    data = db.query(models.Products).all()
    return data

#Response model added, to send only few fields to user
#jsonable_encoder converts model data type to json data type
@router.get("/resp/{id}", status_code=status.HTTP_200_OK, response_model=schema.Response_Model)
def get_all(id:int, db:Session=Depends(get_db), user_detail:dict=Depends(oauth2.get_current_user)):
    data = db.query(models.Products).filter(models.Products.id==id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id = {id} not found.")

    a, b = user_detail
    user_id = a[1]

    if user_id != str(data.user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Others product details cant be seen.")
        
    return data

@router.get("/{id}")
def get_all(id:int, db:Session=Depends(get_db)):
    data = db.query(models.Products).filter(models.Products.id==id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id = {id} not found.")
    return {"data": data}

@router.post("/old-way")
def create_new(payload:schema.Product, db:Session=Depends(get_db)):
    new_product = models.Products(name=payload.name, price=payload.price, is_available=payload.is_available, inventory=payload.inventory)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"data": new_product}

# even if we pass extra key value data in the post request, Schema will ignore
# **payload.dict() this unpacks the body data like dictionary
@router.post("/")
def create_new(payload:schema.Product, db:Session=Depends(get_db), user_detail:dict=Depends(oauth2.get_current_user)):
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