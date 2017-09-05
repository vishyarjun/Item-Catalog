import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Sales_Category(Base):
    __tablename__ = 'sales_category'

    category_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(2000), nullable=True)
    created_by = Column(String(250), nullable=True)
    created_on = Column(DateTime, nullable=True)
    img_url = Column(String(2000), nullable=True)

class User_Details(Base):
    __tablename__ = 'user_details'

    user_email = Column(String(250), primary_key=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=True)
    img = Column(String(2000), nullable=True)

class Sales_Item(Base):
    __tablename__ = 'sales_item'

    item_id = Column(Integer, primary_key = True)
    name =Column(String(250), nullable = False)
    description = Column(String(2000), nullable=True)
    price = Column(String(8))
    created_by = Column(String(250), nullable=True)
    created_on = Column(DateTime, nullable=True)
    category_id = Column(Integer,ForeignKey('sales_category.category_id'))
    user_email = Column(String(250), ForeignKey('user_details.user_email'))
    sales_category = relationship(Sales_Category)
    user_details = relationship(User_Details)

    @property
    def serialize(self):

        return {
            'name': self.name,
            'description': self.description,
            'item_id': self.item_id,
            'price': self.price,
            'created_by': self.created_by,
            'created_on': self.created_on,
        }

engine = create_engine('sqlite:///salescatalog.db')
Base.metadata.create_all(engine)