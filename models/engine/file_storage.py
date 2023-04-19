#!/usr/bin/python3
import json
import os
"""serializes instances to a JSON file\
        and deserializes JSON file to instances"""


class FileStorage:
    """Implementation"""
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns the dictionary"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """sets in the __objects the obj with key <obj classname>.id"""
        # serializing in this method will make object to be
        # saved without instances
        # suppose u serialize here, you must save
        # immediately inorder to store in the disk
        # FileStorage.__objects[obj.__class__.__name__
        # + '.' + obj.id] = obj.to_dict()
        # instead, store the objects in the
        # FileStorage.__objects and serialize in the save() method
        self.__objects[obj.__class__.__name__ + '.' + obj.id] = obj

    def save(self):
        """serializes __objects to the JSON file"""
        dictionary = {}
        for key, values in FileStorage.__objects.items():
            dictionary[key] = values.to_dict()
        with open(FileStorage.__file_path, 'w') as output:
             json.dump(dictionary, output)
                # This will not work well. Object instances wont be saved
                # with open(self.__file_path, 'w') as output:
                # json.dump(FileStorage.__objects, output)

    def reload(self):
        """deserializes the JSON file to __objects only if JSON file\
                exists; otherwise do nothing. If the file doesn't exist\
                no exception should be raised"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.city import City
        from models.amenity import Amenity
        from models.state import State
        from models.review import Review
        dct = {'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'City': City, 'Amenity': Amenity, 'State': State,
               'Review': Review}
        if os.path.exists(self.__file_path) is True:
            with open(self.__file_path, 'r') as f:
                for key, value in json.load(f).items():
                    self.new(dct[value['__class__']](**value))

    def delete(self, obj=None):
        """Deletes obj from __objects if in else do nothing"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]
