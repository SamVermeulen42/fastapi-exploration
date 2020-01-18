from sqlalchemy.orm import Session

from . import model, schema


def get_package(db: Session, name: str):
    return db.query(model.SoftwarePackage).filter(model.SoftwarePackage.name == name).first()


def list_packages(db: Session, offset: int = 0, limit: int = 100):
    return db.query(model.SoftwarePackage).offset(offset).limit(limit).all()
