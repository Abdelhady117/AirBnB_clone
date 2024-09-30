#!/usr/bin/python3

""" This module defines user model. """

from models.base_model import BaseModel


class User(BaseModel):
    """ defines user class that inherits from BaseModel. """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
