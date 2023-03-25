from fastapi import FastAPI
from models import models
from orm_dbconn.orm_db import engine
from routers import product, user, auth, purchase
from config import settings

from fastapi.middleware.cors import CORSMiddleware
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "https://www.google.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(product.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(purchase.router)




