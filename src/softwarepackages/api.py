from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, schema, model
from .database import get_db
from .schema import SoftwarePackageStatus

router = APIRouter()

# if allowed states is not supplied, all states are assumed ok
def validate_package(package, allowed_states=None):
    if package is None:
        raise HTTPException(status_code=404, detail="Package not found")
    if allowed_states is not None and package.status not in allowed_states:
        raise HTTPException(status_code=400, detail="Package has state {}, but that is not in the allowed states.".format(package.status))  # TODO: add the allowed states in the response


@router.get("/ping")
async def ping():
    return "pong"


@router.get("/packages", response_model=List[schema.SoftwarePackage])
def list_packages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    packages = crud.list_packages(db, offset=skip, limit=limit)
    return [vars(p) for p in packages]


@router.get("/packages/{id}", response_model=schema.SoftwarePackage)
def get_package(id: int, db: Session = Depends(get_db)):
    package = crud.get_package_by_id(db, id)
    validate_package(package)
    return vars(package)


@router.delete("/packages/{id}", response_model=schema.SoftwarePackage)
def delete_package(id: int, db: Session = Depends(get_db)):
    count = crud.delete_package_by_id(db, id)
    if count == 0:
        raise HTTPException(status_code=404, detail="Package not found")
    return


@router.post("/packages", response_model=schema.SoftwarePackage)
def create_package(package: schema.SoftwarePackageBase, db: Session = Depends(get_db)):
    db_package = crud.get_package(db, name=package.name, version=package.version)
    if db_package:
        raise HTTPException(status_code=400, detail="The software is already registered in the given version.")
    return vars(crud.create_package(db=db, package=package))


# note: this api can also be used to deactivate a package but the /deactivate api is easier to use
@router.post("/packages/{id}", response_model=schema.SoftwarePackage)
def update_package(id: int, package: schema.SoftwarePackageBase, db: Session = Depends(get_db)):
    db_package = crud.update_package(db, id=id, package=package, status=SoftwarePackageStatus.CREATED)
    if db_package:
        raise HTTPException(status_code=400, detail="The software is already registered in the given version.")
    return vars(crud.create_package(db=db, package=package))


@router.get("/packages/{id}/download", response_model=schema.SoftwarePackage)
def download_package(id: int, db: Session = Depends(get_db)):
    db_package = crud.get_package_by_id(db, id=id)
    validate_package(db_package, [SoftwarePackageStatus.CREATED.value])
    crud.update_package_status(db, id, SoftwarePackageStatus.DOWNLOADED)  # for now instantly
    db.refresh(db_package)
    return vars(db_package)


@router.get("/packages/{id}/activate", response_model=schema.SoftwarePackage)
def activate_package(id: int, db: Session = Depends(get_db)):
    db_package = crud.get_package_by_id(db, id=id)
    validate_package(db_package, [SoftwarePackageStatus.DOWNLOADED.value])
    crud.update_package_status(db, id, SoftwarePackageStatus.ACTIVE)  # for now instantly
    db.refresh(db_package)
    return vars(db_package)


@router.get("/packages/{id}/remove", response_model=schema.SoftwarePackage)
def remove_package(id: int, db: Session = Depends(get_db)):
    db_package = crud.get_package_by_id(db, id=id)
    validate_package(db_package, [SoftwarePackageStatus.DOWNLOADED.value, SoftwarePackageStatus.ACTIVE.value])
    crud.update_package_status(db, id, SoftwarePackageStatus.CREATED)
    db.refresh(db_package)
    return vars(db_package)


@router.get("/packages/{id}/deactivate", response_model=schema.SoftwarePackage)
def deactivate_package(id: int, db: Session = Depends(get_db)):
    db_package = crud.get_package_by_id(db, id=id)
    validate_package(db_package, [SoftwarePackageStatus.ACTIVE.value])
    crud.update_package_status(db, id, SoftwarePackageStatus.DOWNLOADED)
    db.refresh(db_package)
    return vars(db_package)


