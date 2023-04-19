#!/usr/bin/python3
"""
Defines city
"""
from os import getenv
from models.base_model import BaseModel, Base
from models.place import Place
from sqlalchemy import String, Integer, ForeignKey, Column
from sqlalchemy.orm import relationship

HBNB_STORAGE_TYPE = getenv('HBNB_STORAGE_TYPE')
class City(BaseModel, Base):
    """defines city to look for"""
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    places = relationship('Place', backref='cities',
                          cascade="all, delete-orphan")
