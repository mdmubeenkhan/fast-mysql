from fastapi import APIRouter, Depends, status, HTTPException, Response
from schema import schema
from models import models
from sqlalchemy.orm import Session
from orm_dbconn import orm_db

from security import hashing

from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from auth import oauth2

router = APIRouter(
    tags=["Authentication"]
)


#we can write payload or user_credential, or any other meaningful word to get request body
@router.post("/auth")
def login(user_credential:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(orm_db.get_db)):
    # OAuth2PasswordRequestForm always consider "username" and "password", 
    # even if user passes email, it will be treated as username

    #Once we start using OAuth2PasswordRequestForm we can no longer be able to pass user credential in body
    # we need to pass user credential in FORM data

    # def login(user_credential:schema.Auth_Schema, db:Session=Depends(orm_db.get_db)):

    # we have to modify below line use username instead of email as we are using OAuth2PasswordRequestForm
    # user = db.query(models.Users).filter(models.Users.email == user_credential.email).first()

    user = db.query(models.Users).filter(models.Users.email == user_credential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credential.")
    
    if not hashing.verify_pwd(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credential.")

    #apart from user id, we can pass roles and other information also
    #user role hard-coded = Admin
    access_token = oauth2.create_access_token(data={"user_id":user.id, "user_role":"Admin"})

    return {"access_token": access_token, "token_type":"bearer"}