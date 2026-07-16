from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__= 'users'
    id =Column(Integer, primary_key = True, index = True)
    username = Column(String, nullable=False, unique = True)
    email  = Column(String, nullable=False, unique=True)
    password = Column(String)
    role = Column(String, default='user')
    projects = relationship("Project", back_populates = "owner")