from db import Base
from sqlalchemy import Column, Integer, String, JSON

class Profiles(Base):
    __tablename__ = 'profiles'

    id: Column(Integer, primary_key=True)
    user_name: Column(String, nullable=False)
    profile_name: Column(String, nullable=False)
    age: Column(Integer)
    description: Column(String)
    tags: Column()

class Tags(Base):
    __tablename__ = 'tags'

    id: Column(Integer, primary_key=True)
    name: Column(String, nullable=False)