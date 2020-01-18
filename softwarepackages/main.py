# https://fastapi.tiangolo.com/tutorial/sql-databases/
import uvicorn
from fastapi import FastAPI
from softwarepackages import api
from softwarepackages.data import model
from softwarepackages.data.database import engine

model.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(api.router)


def main():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")


if __name__ == "__main__":
    main()
