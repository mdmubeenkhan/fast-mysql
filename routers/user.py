from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from orm_dbconn.orm_db import get_db
from models import models
from typing import List
from schema import schema
from security import hashing

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
def create_new(payload:schema.CreateUser, db:Session=Depends(get_db)):
    payload.password = hashing.hash_pwd(payload.password)
    new_user = models.Users(**payload.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schema.UserResponse])
def get_all(db:Session=Depends(get_db)):
    data = db.query(models.Users).all()
    return data


@router.get("/get-user/{id}", status_code=status.HTTP_200_OK, response_model=schema.UserResponse)
def get_all(id:int, db:Session=Depends(get_db)):
    data = db.query(models.Users).filter(models.Users.id==id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id = {id} not found.")
    return data