from enum import Enum, auto

from pydantic import BaseModel


class SoftwarePackageStatus(Enum):
    CREATED = 'CREATED'
    DOWNLOADED = 'DOWNLOADED'
    ACTIVE = 'ACTIVE'


class SoftwarePackageBase(BaseModel):
    name: str
    version: str


class SoftwarePackage(SoftwarePackageBase):
    id: int
    status: str
