from sqlalchemy.orm import Session

from softwarepackages.data import schema, model


def get_package(db: Session, name: str, version: str):
    return db.query(model.SoftwarePackage)\
        .filter(model.SoftwarePackage.name == name)\
        .filter(model.SoftwarePackage.version == version)\
        .first()


def get_package_by_id(db: Session, id: int):
    return db.query(model.SoftwarePackage).filter(model.SoftwarePackage.id == id).first()


def delete_package_by_id(db: Session, id: int):
    result = db.query(model.SoftwarePackage.id == id).delete()
    db.commit()
    return result


def list_packages(db: Session, offset: int = 0, limit: int = 100):
    return db.query(model.SoftwarePackage).offset(offset).limit(limit).all()


def create_package(db: Session, package: schema.SoftwarePackageBase):
    new_package = model.SoftwarePackage(name=package.name, version=package.version,
                                        status=schema.SoftwarePackageStatus.CREATED.value)
    db.add(new_package)
    db.commit()
    db.refresh(new_package)
    return new_package


def update_package(db: Session, id: int, package: schema.SoftwarePackageBase,
                   status: schema.SoftwarePackageStatus = schema.SoftwarePackageStatus.CREATED):
    found_package = db.query(model.SoftwarePackage).filter(model.SoftwarePackage.id == id).first()
    if found_package:
        return None
    found_package.update(**vars(package), **{'status': status.value})
    db.commit()
    db.refresh(found_package)
    return found_package


def update_package_status(db: Session, id: int, status: schema.SoftwarePackageStatus):
    db.query(model.SoftwarePackage).filter(model.SoftwarePackage.id == id).update({'status': status.value})
    db.commit()

