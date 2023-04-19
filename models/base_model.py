#!/usr/bin/env python3
import uuid
import models
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Integer, Column, ForeignKey, DateTime

"""Base model class"""


Base = declarative_base()
class BaseModel:
    """defines all common attributes/methods for other classes"""
    #__tablename__ = 'base'
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialize Base Model class
        Args:
            args(tuple): tuple argument. Won't be used here
            kwargs(dict): object dictionary passed
        Attributes:
            id: unique number for identification
            created_at: shows when the object was created
            updated_at: shows when the object was last updated
            storage
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__" and key != '_sa_instance_state':
                    setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.now()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()


    def __str__(self):
        """returns string representation of an object"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def __repr__(self):
        """returns official string representation"""
        return self.__str__()

    def save(self):
        """updates the object date"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values\
                of __dict__ instance"""
        objec = {}
        for key in self.__dict__:
            if key == 'created_at' or key == 'updated_at':
                objec[key] = self.__dict__[key].isoformat()
            else:
                objec[key] = self.__dict__[key]
        objec['__class__'] = self.__class__.__name__
        if "_sa_instance_state" in objec:
            del objec["_sa_instance_state"]
        return objec

    def delete(self):
        """Returns current instance from the storage"""
        models.storage.delete(self)
