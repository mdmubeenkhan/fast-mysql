from fastapi import FastAPI
from models import models
from orm_dbconn.orm_db import engine
from routers import product, user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(product.router)
app.include_router(user.router)


