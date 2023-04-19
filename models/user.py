#!/usr/bin/python3
from models.place import Place
from models.base_model import BaseModel, Base
from models.review import Review
from sqlalchemy.orm import relationship
from sqlalchemy import String, Column
"""Inherits basemodel"""


class User(BaseModel, Base):
    """Implementation"""
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    places = relationship("Place", backref='user',
                           cascade='all, delete-orphan')
    reviews = relationship("Review", backref='user',
                           cascade='all, delete-orphan')
