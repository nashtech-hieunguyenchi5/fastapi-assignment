from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from entities.base_entity import BaseEntity

class Company(BaseEntity, Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    mode = Column(String)
    rating = Column(Integer)

    users = relationship("User", back_populates="company")