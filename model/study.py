import enum
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from  model import Base, Category

class PriorityEnum(str, enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"

class StatusEnum(str, enum.Enum):
    uncompleted = "uncompleted"
    completed = "completed"

class Study(Base):
    __tablename__ = 'study'

    id = Column("pk_study", Integer, primary_key=True)
    title = Column(String(225))
    description = Column(String(225))
    content = Column(String(225))
    status = Column(Enum(StatusEnum))
    priority = Column(Enum(PriorityEnum))
    
    # Cada study pode ter uma category
    category_id = Column(Integer, ForeignKey(Category.id), nullable=True)
    category = relationship("Category")

    def __init__(self, title:str, description:int, content:float,
                 priority: str, category_id: int = None):
        """
        Cria um Study
        Arguments:
            title: titulo do conteudo para ser estudado
            description: descrição do conteudo para estudo.
            content: o conteudo a ser estudado
            status: status para definir se o estudo foi ou não concluido
            priority: qual a prioridade do estudo, pode ser: high, medium ou low
        """
        self.title = title
        self.description = description
        self.content = content
        self.status = "uncompleted"
        self.priority = priority
        self.category_id = category_id
