from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from . import crud, schema
from .database import get_db

router = APIRouter()


@router.get("/ping")
async def ping():
    return "pong"


@router.get("/packages", response_model=List[schema.SoftwarePackage])
def list_packages(skip: int=0, limit: int = 100, db: Session = Depends(get_db)):
    packages = crud.list_packages(db)
    return packages


@router.get("/packages", response_model=List[schema.SoftwarePackage])
def list_packages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    packages = crud.list_packages(db, offset=skip, limit=limit)
    return packages
