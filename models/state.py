#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
import models
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City


class State(BaseModel, Base):
    """ State class """
    if models.session_type == "db":
        __tablename__ = "states"

        name = Column(String(128), nullable=False)
        cities = relationship(
                "City", back_populates="state", cascade="all, delete-orphan"
            )
    else:
        name = ""

    if models.session_type != "db":
        @property
        def cities(self):
            city_list = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
