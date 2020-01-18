from enum import Enum, auto


class SoftwarePackage:
    def __init__(self, name, version):
        self.name = name
        self.version = version
        self.status = SoftwarePackageStatus.CREATED


class SoftwarePackageStatus(Enum):
    CREATED = auto()
    DOWNLOADED = auto()
    ACTIVE = auto()

