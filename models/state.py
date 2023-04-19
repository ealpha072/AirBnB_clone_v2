#!/usr/bin/python3
"""
Class that defines a state
"""
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Column
from os import getenv

storage_t = getenv('HBNB_STORAGE_TYPE')

class State(BaseModel, Base):
    """class to create a state"""
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if storage_t == 'db':
        cities = relationship('City', backref='states',
                              cascade='all, delete-orphan')
    else:
        @property
        def cities(self):
            """getter for list of city instances related to the state"""
            city_list = []
            all_cities = models.storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
