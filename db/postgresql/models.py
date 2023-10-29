from .db import Base
from sqlalchemy import Integer, String, Column

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True)
    username = Column(String, nullable=False)