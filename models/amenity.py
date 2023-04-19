#!/usr/bin/python3
"""
Defines amenities
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from models.place import place_amenity


class Amenity(BaseModel, Base):
    """Defines amenities that user can choose from to offer at its place"""
    __tablename__ = "amenities"
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        place_amenities = relationship("Place", secondary=place_amenity,
                                       back_populates='amenities')
    else:
        name=''
