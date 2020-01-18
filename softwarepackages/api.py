import time
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket
from fastapi.security import APIKeyHeader

from jinja2 import Environment, BaseLoader

from .data import schema, crud
from softwarepackages.data.database import get_db
from softwarepackages.data.schema import SoftwarePackageStatus
from .data.model import APIKey

router = APIRouter()

api_key_header = APIKeyHeader(name='access_token', auto_error=False)

html = """
<!DOCTYPE html>
<html>
    <body>
        <p id="message">Connecting...</p>
        <script>
            var ws = new WebSocket("ws://localhost:8000/packages/{{ id }}/{{ ws }}");
            ws.onmessage = function(event) {
                document.getElementById("message").innerHTML = event.data;
            };
        </script>
    </body>
</html>
"""
rtemplate = Environment(loader=BaseLoader).from_string(html)


# Dependency
async def get_api_key():
    supplied_key = Security(api_key_header)
    if crud.validate_api_key:
        raise HTTPException(status_code=403, detail="Api key (header) did not match an allowed api key")
    return supplied_key


# if allowed states is not supplied, all states are assumed ok
def validate_package(package, allowed_states=None):
    if package is None:
        raise HTTPException(status_code=404, detail="Package not found")
    if allowed_states is not None and package.status not in allowed_states:
        raise HTTPException(status_code=400, detail="Package has state {}, but that is not in the allowed states.".format(package.status))  # TODO: add the allowed states in the response


@router.get("/ping")
async def ping(api_key: APIKey = Depends(get_api_key)):
    return "pong"


@router.get("/packages", response_model=List[schema.SoftwarePackage])
def list_packages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _: APIKey = Depends(get_api_key)):
    packages = crud.list_packages(db, offset=skip, limit=limit)
    return [vars(p) for p in packages]


@router.get("/packages/{id}", response_model=schema.SoftwarePackage)
def get_package(id: int, db: Session = Depends(get_db), _: APIKey = Depends(get_api_key)):
    package = crud.get_package_by_id(db, id)
    validate_package(package)
    return vars(package)


@router.delete("/packages/{id}", response_model=schema.SoftwarePackage)
def delete_package(id: int, db: Session = Depends(get_db), _: APIKey = Depends(get_api_key)):
    count = crud.delete_package_by_id(db, id)
    if count == 0:
        raise HTTPException(status_code=404, detail="Package not found")
    return


@router.post("/packages", response_model=schema.SoftwarePackage)
def create_package(package: schema.SoftwarePackageBase, db: Session = Depends(get_db), _: APIKey = Depends(get_api_key)):
    db_package = crud.get_package(db, name=package.name, version=package.version)
    if db_package:
        raise HTTPException(status_code=400, detail="The software is already registered in the given version.")
    return vars(crud.create_package(db=db, package=package))


# note: this api can also be used to deactivate a package but the /deactivate api is easier to use
@router.post("/packages/{id}", response_model=schema.SoftwarePackage)
def update_package(id: int, package: schema.SoftwarePackageBase, db: Session = Depends(get_db), _: APIKey = Depends(get_api_key)):
    db_package = crud.update_package(db, id=id, package=package, status=SoftwarePackageStatus.CREATED)
    if db_package:
        raise HTTPException(status_code=400, detail="The software is already registered in the given version.")
    return vars(crud.create_package(db=db, package=package))


@router.get("/packages/{id}/remove", response_model=schema.SoftwarePackage)
def remove_package(id: int, db: Session = Depends(get_db), _: APIKey = Depends(get_api_key)):
    db_package = crud.get_package_by_id(db, id=id)
    validate_package(db_package, [SoftwarePackageStatus.DOWNLOADED.value, SoftwarePackageStatus.ACTIVE.value])
    crud.update_package_status(db, id, SoftwarePackageStatus.CREATED)
    db.refresh(db_package)
    return vars(db_package)


@router.get("/packages/{id}/deactivate", response_model=schema.SoftwarePackage)
def deactivate_package(id: int, db: Session = Depends(get_db), _: APIKey = Depends(get_api_key)):
    db_package = crud.get_package_by_id(db, id=id)
    validate_package(db_package, [SoftwarePackageStatus.ACTIVE.value])
    crud.update_package_status(db, id, SoftwarePackageStatus.DOWNLOADED)
    db.refresh(db_package)
    return vars(db_package)


@router.get("/packages/{id}/download", response_model=schema.SoftwarePackage)
def download_package(id: int, db: Session = Depends(get_db), _: APIKey = Depends(get_api_key)):
    db_package = crud.get_package_by_id(db, id=id)
    validate_package(db_package, [SoftwarePackageStatus.CREATED.value])
    return HTMLResponse(rtemplate.render({'id': id, 'ws': 'download/ws'}))


@router.websocket("/packages/{id}/download/ws")
async def websocket_endpoint_download(id: int, websocket: WebSocket, db: Session = Depends(get_db), _: APIKey = Depends(get_api_key)):
    await websocket.accept()
    for message in download_package_internal():
        await websocket.send_text(message)
    crud.update_package_status(db, id, SoftwarePackageStatus.DOWNLOADED)
    await websocket.send_text('Download complete')


def download_package_internal():
    for p in range(0, 101, 5):
        time.sleep(0.5)
        yield 'Download progress: {}'.format(p)


@router.get("/packages/{id}/activate", response_model=schema.SoftwarePackage)
def activate_package(id: int, db: Session = Depends(get_db), _: APIKey = Depends(get_api_key)):
    db_package = crud.get_package_by_id(db, id=id)
    validate_package(db_package, [SoftwarePackageStatus.DOWNLOADED.value])
    crud.deactivate_packages_by_name(db, db_package.name)
    return HTMLResponse(rtemplate.render({'id': id, 'ws': 'activate/ws'}))


@router.websocket("/packages/{id}/activate/ws")
async def websocket_endpoint_activate(id: int, websocket: WebSocket, db: Session = Depends(get_db), _: APIKey = Depends(get_api_key)):
    await websocket.accept()
    for message in activate_package_internal():
        await websocket.send_text(message)
    crud.update_package_status(db, id, SoftwarePackageStatus.ACTIVE)
    await websocket.send_text('Activation complete')


def activate_package_internal():
    yield 'Gathering information on your package'
    time.sleep(1)
    yield 'Activating the package'
    time.sleep(4)

