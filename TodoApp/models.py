from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String)
    contacts = relationship("Contact", back_populates="user")


class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))


class Province(Base):
    __tablename__ = "provinces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    cities = relationship("City", back_populates="province")


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    province_id = Column(Integer, ForeignKey("provinces.id"))

    province = relationship("Province", back_populates="cities")
    addresses = relationship("Address", back_populates="city")


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)

    street = Column(String, nullable=False)

    city_id = Column(Integer, ForeignKey("cities.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    city = relationship("City", back_populates="addresses")
    user = relationship("Users", back_populates="addresses")
