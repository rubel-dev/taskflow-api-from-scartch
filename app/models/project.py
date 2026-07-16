 
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable = False)
    description = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String)
    created_at = Column(Date)
    owner = relationship("User", back_populates = "projects")
    tasks = relationship("Task", back_populates='project')