#!/usr/bin/python3
"""
Defines review class
"""
from models.base_model import BaseModel, Base
from sqlalchemy import String, Integer, Column, ForeignKey


class Review(BaseModel, Base):
    """Reviews made by users about a place"""
    __tablename__ = 'reviews'
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    text = Column(String(1024), nullable=False)
