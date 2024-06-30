import enum
from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship

from  model import Base

class Category(Base):
    __tablename__ = 'category'

    id = Column("pk_category", Integer, primary_key=True)
    name = Column(String(225), unique=True)

    def __init__(self, name:str):
        """
        Cria um Category
        Arguments:
            id: id da categoria
            name: nome da categoria
        """
        self.name = name
