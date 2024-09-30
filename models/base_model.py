#!/usr/bin/python3

""" This module defines the BaseModel class. """

import uuid
from datetime import datetime
import models


class BaseModel:
    """ defines all common attributes/methods for other classes. """

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance for the BaseModel.
        *args: won't be used
        **kwargs: a dictionary of key-values arguments
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key in ["created_at", "updated_at"]:
                        value = datetime.strptime(
                            value, "%Y-%m-%dT%H:%M:%S.%f")
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """
        Returns a string representation of the instance in format:
            [<class name>] (<self.id>) <self.__dict__>
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        updates the attribute updated_at with the current datetime
        saves the instance.
        """
        self.updated_at = datetime.utcnow()
        models.storage.save()

    def to_dict(self):
        """
        return a dictionary containing all keys/values of __dict__ of instance
        """
        # copy the dictionary to avoid changing the original
        obj_dict = dict(self.__dict__)
        # obj_dict = self.__dict__.copy()
        obj_dict["__class__"] = self.__class__.__name__
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        return obj_dict
