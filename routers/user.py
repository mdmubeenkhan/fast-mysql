from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from orm_dbconn.orm_db import get_db
from models import models
from typing import List
from schema import schema
from security import hashing
from auth import oauth2

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

@router.delete("/{id}")
def delete_user(id:int, db:Session=Depends(get_db), user_detail:dict=Depends(oauth2.get_current_user)):
    data = db.query(models.Users).filter(models.Users.id==id)
    if not data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id = {id} not found.")
    data.delete(synchronize_session=False)
    db.commit()
    return {"details":f"User with id = {id} is deleted."}