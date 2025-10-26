from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    projects = relationship('Project', back_populates='owner')

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String, index=True)
    description = Column(Text, default='')
    archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner = relationship('User', back_populates='projects')
    subcategories = relationship('Subcategory', back_populates='project', cascade='all, delete')

class Subcategory(Base):
    __tablename__ = 'subcategories'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    title = Column(String)
    details = Column(Text, default='')
    progress = Column(Integer, default=0)
    due_date = Column(DateTime, nullable=True)
    notified = Column(Boolean, default=False)
    project = relationship('Project', back_populates='subcategories')

class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    subcategory_id = Column(Integer, ForeignKey('subcategories.id'))
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
