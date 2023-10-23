#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is not None:
            objs = {}
            for k, v in FileStorage.__objects.items():
                if isinstance(v, cls):
                    objs[k] = v
            return objs
        else:
            return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """
        Deserializes the JSON objects in file.json to a python dictionary
        format then pass it as a kwargs to BaseModel constructor to convert it
        BaseModel class representing format
        """
        try:
            with open(self.__file_path, "r", encoding='utf-8') as f:
                json_objs = json.load(f)
            models = {
                'User': User,
                'BaseModel': BaseModel,
                'State': State,
                'City': City,
                'Amenity': Amenity,
                'Place': Place,
                'Review': Review
            }
            for key, val in json_objs.items():
                constractor = val["__class__"]
                for model, cls in models.items():
                    if constractor == model:
                        self.__objects[key] = cls(**val)
        except FileNotFoundError:
            pass
        except Exception as e:
            pass

    def delete(self, obj=None):
        """ delete obj from __objects"""
        if obj is not None:
            my_obj = obj.to_dict()['__class__'] + '.' + obj.id
            if my_obj in FileStorage.__objects:
                del FileStorage.__objects[my_obj]
                self.save()

    def close(self):
        """ Method for deserializing the JSON file to objects"""
        self.reload()
