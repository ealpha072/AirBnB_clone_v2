#!/usr/bin/python3

"""database storage"""

from os import getenv
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.city import City
from models.user import User
from models.state import State
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}
Base = declarative_base()
class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """Implemeting"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB),
                                      pool_pre_ping=True)
        if HBNB_ENV == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """query current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)


    def new(self, obj):
        """Adds new object to current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """commit all changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes from current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.close()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or None if not
        found
        """
        objects = self.__session.query(classes[cls])
        for obj in objects:
            if obj.id == id:
                return obj
        return None

    def count(self, cls=None):
        """
        Returns the number of objects in storage matching the given class name.
        If no name is passed, returns the count of all objects in storage.
        """
        nobjects = 0
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                nobjects += len(self.__session.query(classes[clss]).all())
        return nobjects
