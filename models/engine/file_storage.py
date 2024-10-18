#!/usr/bin/python3

"""
This module defines FileStorage class that
- serializes instances to JSON file
- deserializes JSON file to instances.
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """ defines the FileStorage class. """

    # path to the json file
    __file_path = "file.json"
    # A dictionary to store all objects by <obj class name>.id
    __objects = {}

    def all(self):
        """Returns all the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        obj_dict = {key: obj.to_dict()
                    for key, obj in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, 'w') as file:
            json.dump(obj_dict, file)

    def reload(self):
        """Deserializes the JSON file to __objects if the JSON file exists"""
        try:
            with open(FileStorage.__file_path, 'r') as f:
                # load the json data from the file to a python dictionary
                obj_dict = json.load(f)
                for key, obj_data in obj_dict.items():
                    cls_name = obj_data["__class__"]
                    # cls_name = key.split('.')[0]

                    # use the class name to create an instance of that class
                    obj = globals()[cls_name](**obj_data)
                    # obj = eval(cls_name)(**obj_data)
                    # store the instance in __objects
                    FileStorage.__objects[key] = obj
        except (FileNotFoundError, PermissionError):
            # if the file does not exist, do nothing
            pass
