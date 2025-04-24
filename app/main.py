from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
import app.models 

app = FastAPI()

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "FastAPI + Postgres are live"}