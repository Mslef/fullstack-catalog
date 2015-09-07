# -*- coding: utf_8 -*-

import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    '''User data structure'''
    __tablename__ = 'user'
    name = Column (String(250), nullable = False)
    email = Column (String(250), primary_key = True, nullable = False)
    picture = Column (String(250))
    admin = Column(Boolean, nullable = False)

class Category(Base):
    '''Category data structure'''
    __tablename__ = 'category'

    name = Column (String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    user_id = Column(String(250), ForeignKey('user.email'))
    user = relationship(User)

    @property
    def serialize(self):
        '''Returns object data in serializeable format '''
        return {
            'name':self.name,
            'id':self.id
        }

class Item(Base):
    '''Item data structure'''
    __tablename__ = 'item'

    name = Column (String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(Unicode(250))
    image_url = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(String(250), ForeignKey('user.email'))
    user = relationship(User)

    @property
    def serialize(self):
        '''Returns object data in serializeable format '''
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'image url': self.image_url
        }

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
