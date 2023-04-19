#!/usr/bin/python3
"""
Defines Place class
"""
from os import getenv
import models
from models.base_model import BaseModel, Base
from models.review import Review
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

HBNB_TYPE_STORAGE = getenv('HBNB_TYPE_STORAGE')

place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60),
                             ForeignKey("places.id"),
                             primary_key=True,
                             nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """Defines Place class"""
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    number_rooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, default=0.0, nullable=False)
    longitude = Column(Float, default=0.0, nullable=False)
    amenity_ids = []

    if HBNB_TYPE_STORAGE == 'db':
        reviews = relationship('Review', backref='place')
        amenities = relationship('Amenity', back_populates='place_amenities',
                                 secondary=place_amenity, viewonly=False)

    else:
        @property
        def reviews(self):
            """returns the reviews for the FileStorage"""
            n_list = []
            reload_review = models.storage.all(Review)
            for key, value in reload_review:
                if value['place_id'] == Place.id:
                   n_list.append(value)
            return n_list
        
        @property
        def amenities(self):
            """handles append method for adding amenity.id\
                    to amenity_ids"""
            return self.amenity_ids

        @amenities.setter
        def amenities(self, cls=None):
            """sets the amenity ids"""
            from models.amenity import Amenity
            if cls is None or cls.__class__ ==  Amenity:
                add_amenity = models.storage.all(Amenity)
                for key in add_amenity:
                    self.amenity_ids.append(add_amenity[key])
