from enum import Enum, auto

from pydantic import BaseModel


class SoftwarePackageStatus(Enum):
    CREATED = auto()
    DOWNLOADED = auto()
    ACTIVE = auto()


class SoftwarePackage(BaseModel):
    name: str
    version: str
    status: SoftwarePackageStatus
