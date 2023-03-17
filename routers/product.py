
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from orm_dbconn.orm_db import get_db
from models import models
from fastapi.encoders import jsonable_encoder
from typing import List
from schema import schema


router = APIRouter(
    prefix="/product",
    tags=["Product"]
)

@router.get("/")
def get_all(db:Session=Depends(get_db)):
    data = db.query(models.Products).all()
    return {"data": data}

#Response model added, to send only few fields to user
@router.get("/resp", status_code=status.HTTP_200_OK, response_model=List[schema.Response_Model])
def get_all(db:Session=Depends(get_db)):
    data = db.query(models.Products).all()
    return data

#Response model added, to send only few fields to user
#jsonable_encoder converts model data type to json data type
@router.get("/resp/{id}", status_code=status.HTTP_200_OK, response_model=schema.Response_Model)
def get_all(id:int, db:Session=Depends(get_db)):
    data = db.query(models.Products).filter(models.Products.id==id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id = {id} not found.")
    return jsonable_encoder(data)

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
def create_new(payload:schema.Product, db:Session=Depends(get_db)):
    new_product = models.Products(**payload.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"data": new_product}

@router.delete("/{id}")
def delete_product(id:int, db:Session=Depends(get_db)):
    data = db.query(models.Products).filter(models.Products.id==id)
    if not data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id = {id} not found.")
    data.delete(synchronize_session=False)
    db.commit()
    return {"details":f"Record with id = {id} is deleted."}


@router.put("/{id}")
def update(id:int, payload:schema.Product, db:Session=Depends(get_db)):
    data = db.query(models.Products).filter(models.Products.id==id)
    if not data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id = {id} not found.")
    data.update(payload.dict(), synchronize_session=False)
    db.commit()
    return {"data": data.first()}