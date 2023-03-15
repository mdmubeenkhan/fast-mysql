from fastapi import FastAPI, Depends, HTTPException, status
from models import models
from orm_dbconn.orm_db import engine
from sqlalchemy.orm import Session
from orm_dbconn.orm_db import get_db
from schema import schema

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def get_all(db:Session=Depends(get_db)):
    data = db.query(models.Products).all()
    return {"data": data}

@app.get("/{id}")
def get_all(id:int, db:Session=Depends(get_db)):
    data = db.query(models.Products).filter(models.Products.id==id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id = {id} not found.")
    return {"data": data}

@app.post("/old-way")
def create_new(payload:schema.Product, db:Session=Depends(get_db)):
    new_product = models.Products(name=payload.name, price=payload.price, is_available=payload.is_available, inventory=payload.inventory)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"data": new_product}

# even if we pass extra key value data in the post request, Schema will ignore
# **payload.dict() this unpacks the body data like dictionary
@app.post("/")
def create_new(payload:schema.Product, db:Session=Depends(get_db)):
    new_product = models.Products(**payload.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"data": new_product}

@app.delete("/{id}")
def delete_product(id:int, db:Session=Depends(get_db)):
    data = db.query(models.Products).filter(models.Products.id==id)
    if not data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id = {id} not found.")
    data.delete(synchronize_session=False)
    db.commit()
    return {"details":f"Record with id = {id} is deleted."}


@app.put("/{id}")
def update(id:int, payload:schema.Product, db:Session=Depends(get_db)):
    data = db.query(models.Products).filter(models.Products.id==id)
    if not data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id = {id} not found.")
    data.update(payload.dict(), synchronize_session=False)
    db.commit()
    return {"data": data.first()}



