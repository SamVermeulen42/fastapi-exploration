# https://fastapi.tiangolo.com/tutorial/sql-databases/

from fastapi import FastAPI
from .softwarepackages import api, model
from .softwarepackages.database import engine

model.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(api.router)
