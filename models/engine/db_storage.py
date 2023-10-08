#!/usr/bin/python3
""" New engine DBStorage """
from sqlalchemy import create_engine
from os import getenv
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """ Class DBStorage for SQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """ Initializes a new DB storage instance """

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                getenv("HBNB_MYSQL_USER"),
                getenv("HBNB_MYSQL_PWD"),
                getenv("HBNB_MYSQL_HOST"),
                getenv("HBNB_MYSQL_DB"),
                pool_pre_ping=True
            )
        )

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Query the current database """

        result = {}
        if cls is None:
            classes_to_query = [
                    Review, User, State, City,
                    Amenity, Place
                ]
        else:
            classes_to_query = [cls]

        for class_name in classes_to_query:
            objects = self.__session.query(class_name).all()

            for obj in objects:
                key = "{}.{}".format(class_name.__name__, obj.id)
                result[key] = obj
        return result

    def new(self, obj):
        """ Adds obj to the current DB session """

        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current DB session """

        self.__session.commit()

    def delete(self, obj=None):
        """ Deletes obj from the current DB session """

        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Creates all tables in the database """

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session()
