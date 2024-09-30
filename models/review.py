#!/usr/bin/python3

""" This module defines the review model. """

from models.base_model import BaseModel


class Review(BaseModel):
    """ defines the review class that inherits from BaseModel. """

    place_id = ""
    user_id = ""
    text = ""
