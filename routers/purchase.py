from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from orm_dbconn.orm_db import get_db
from models import models
# from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from schema import schema
from auth import oauth2


router = APIRouter(
    prefix="/purchase",
    tags=["Purchase"]
)

# **payload.dict() this unpacks the body data like dictionary
@router.post("/")
def purchase(payload:schema.Purchase, db:Session=Depends(get_db), user_detail:dict=Depends(oauth2.get_current_user)):
    # verifying that the product user want to purchase is exists in the Product table
    product = db.query(models.Products).filter(models.Products.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id = {payload.product_id} does NOT EXISTS in the Product table.")
    a, b = user_detail
    user_id = a[1]
    print(user_id)
    new_dict = payload.dict()
    new_dict.update({"user_id": user_id})
    # new_product = models.Products(**payload.dict())
    try:
        order = models.Purchase(**new_dict)
        
        db.add(order)
        db.commit()
        db.refresh(order)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Duplicate order of same product is NOT ALLOWED.")
    return {"data": order}


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schema.PurchaseResponse])
def get_all(db:Session=Depends(get_db), user_detail:dict=Depends(oauth2.get_current_user)):
    data = db.query(models.Purchase).all()
    return data