from fastapi import FastAPI, Security
from app.auth import get_current_user
from app.db.base import Base
from app.db.session import engine
from app.api import auth, dataset, user, dataset_row

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(dataset.router)
app.include_router(dataset_row.router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "FastAPI + Postgres are live"}
