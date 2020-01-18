from enum import Enum, auto
from .database import Base
from sqlalchemy import Column, String, Integer, Enum


class SoftwarePackage(Base):
    __tablename__ = "packages"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    version = Column(String)
    status = Column(String)

