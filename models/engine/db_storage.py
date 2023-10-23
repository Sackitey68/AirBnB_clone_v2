#!/usr/bin/python3
"""This module defines a class to manage file DB storage for hbnb clone"""

from os import getenv
from sqlalchemy import create_engine
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {
    'User': User, 'Place': Place,
    'State': State, 'City': City, 'Amenity': Amenity,
    'Review': Review
}


class DBStorage:
    """ This manages the database storage"""
    __engine = None
    __session = None

    def __init__(self):
        """ This instantiate a DBStorage object"""

        dialect = 'mysql'
        driver = 'mysqldb'
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')

        self.__engine = create_engine('{}+{}://{}:{}@{}/{}'.
                                      format(dialect, driver, HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD, HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB),
                                      pool_pre_ping=True)

        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ This returns a dictionary of models currently in DB storage"""
        dic = {}
        if cls is None:
            classes = [State, City, User, Place]
            for model in classes:
                for obj in self.__session.query(model).all():
                    dic[f"{model.__name__}.{obj.id}"] = obj
        else:
            for obj in self.__session.query(cls):
                dic[f"{obj.__class__.__name__}.{obj.id}"] = obj

        return dic

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """This Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete obj from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """reloads objects and prepare the database"""
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session)

    def close(self):
        """call remove() method on the private session"""
        self.__session.close()
