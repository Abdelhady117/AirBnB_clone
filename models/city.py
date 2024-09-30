#!/use/bin/python3

""" This module defines the City model. """

from models.base_model import BaseModel


class City(BaseModel):
    """ Defines the City class that inherits from the BaseModel class. """
    state_id = ""
    name = ""
