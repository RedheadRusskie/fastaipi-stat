from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base
from app.db.session import engine
from app.api import auth, dataset, user, dataset_row

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(dataset.router)
app.include_router(dataset_row.router)


@app.on_event("startup")
def on_startup():
    """
    Only create tables if an actual engine exists.
    This avoids CI/test errors when engine is mocked in tests.
    """
    if engine is not None:
        Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "FastAPI + Postgres are live"}
