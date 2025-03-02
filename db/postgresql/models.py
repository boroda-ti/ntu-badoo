from .db import Base
from sqlalchemy import Integer, String, Column

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(String, unique=True)
    username = Column(String, nullable=True)