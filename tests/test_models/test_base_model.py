#!/usr/bin/python3
"""
Unittest for BaseModel class
"""
import unittest
from models.my_model import BaseModel
from datetime import datetime
import os


class TestBaseModel(unittest.TestCase):
    """ Test suite for BaseModel class """

    def setUp(self):
        """ instantiate a BaseModel instance """
        self.my_model = BaseModel()

    def tearDown(self):
        """ clean up after each test """
        del self.my_model

    def test_instance_creation(self):
        """ Test that a BaseModel instance is created correctly """
        # check if my_model is an instance of BaseModel
        self.assertIsInstance(self.my_model, BaseModel)
        # check if my_model has id attribute
        self.assertTrue(hasattr(self.my_model, 'id'))
        # check if id is string
        self.assertIsInstance(self.my_model.id, str)
        # check if my_model has created_at attribute
        self.assertTrue(hasattr(self.my_model, 'created_at'))
        # check if created_at is a datetime object
        self.assertIsInstance(self.my_model.created_at, datetime)
        # check if my_model has updated_at attribute
        self.assertTrue(hasattr(self.my_model, 'updated_at'))
        # check if updated_at is a datetime instance
        self.assertIsInstance(self.my_model.updated_at, datetime)
        # check that created_at and updated_at are equal at creation
        self.assertEqual(self.my_model.created_at, self.my_model.updated_at)
        # check that each BaseModel instance has a unique id
        temp_model = BaseModel()
        self.assertNotEqual(self.my_model.id, temp_model.id)

    def test_init_with_kwargs(self):
        """Test instantiation with kwargs."""
        model_dict = self.my_model.to_dict()
        kwargs_model = BaseModel(**model_dict)
        # ensure the kwargs_model is a BaseModel
        self.assertIsInstance(kwargs_model, BaseModel)
        # ensure all attributes are correctly set
        self.assertEqual(kwargs_model.id, self.my_model.id)
        self.assertEqual(kwargs_model.created_at, self.my_model.created_at)
        self.assertEqual(kwargs_model.updated_at, self.my_model.updated_at)
        self.assertEqual(kwargs_model.name, self.my_model.name)
        self.assertEqual(kwargs.my_number, self.my_model.name)
        # ensure __class__ is not an attribute of the new instance
        self.assertFalse(hasattr(kwargs_model, "__class__"))
        # ensure the two objects are different
        self.assertNotEqual(kwargs_model, self.my_model)

    def test_kwargs_missing_keys(self):
        """ Test behavior when kwargs is missing keys. """
        model_dict = self.my_model.to_dict()
        # make some keys missing
        del my_model["created_at"]
        del my_model["updated_at"]
        kwargs_model = BaseModel(**model_dict)
        # ensure missing keys are newly set
        self.assertTrue(isinstance(kwargs_model.created_at, datetime))
        self.aseertTrue(isinstance(kwargs_model.updated_at, datetime))

    def test_str_representation(self):
        """ Test the __str__ method for BaseModel. """
        exp_str = f"[BaseModel] ({self.my_model.id} {self.my_model.__dict__})"
        self.assertEqual(str(self.my_model), exp_str)

    def test_save_method(self):
        """ Test the save method for BaseModel. """
        initial_updated_at = self.my_model.updated_at
        self.my_model.save()
        # ensure updated_at has changed
        self.assertNotEqual(initial_updated_at, self.my_model.updated_at)
        # ensure updated_at is later than before
        self.assertGreater(self.my_model.updated_at, initial_updated_at)

    def test_to_dict_method(self):
        """ Test the to_dict methos foe the BaseModel. """
        model_dict = self.my_model.to_dict()
        # ensure that the returned dictionary has the correct type
        self.assertIsInstance(model_dict, dict)
        # check for the presence of all expected keys
        self.assertIn("__class__", model_dict)
        self.assertIn("id", model_dict)
        self.assertIn("created_at", model_dict)
        self.assertIn("updated_at", model_dict)
        # verify the __class__ key has the correct value
        self.assertEqual(model_dict["__class__"], "BaseModel")
        # verify the created_at and updated_at are converted to isoformat
        # strings
        self.assertEqual(
            model_dict["created_at"],
            self.my_model.created_at.isoformat())
        self.assertEqual(
            model_dict["updated_at"],
            self.my_model.updated_at.isoformat())


if __name__ == '__main__':
    unittest.main()
