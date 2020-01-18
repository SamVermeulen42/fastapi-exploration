from enum import Enum, auto
from .database import Base
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import ENUM


class SoftwarePackage(Base):
    __tablename__ = "packages"
    name = Column(String, primary_key=True)
    version = Column(String, primary_key=True)
    status = Column(ENUM('CREATED', 'DOWNLOADED', 'ACTIVE', name='status'))

