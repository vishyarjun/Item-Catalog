import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# The following class is a representation of the DB Table sales_category which
# is a primary variant under which all cars will be available
class Sales_Category(Base):
    __tablename__ = 'sales_category'

    category_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(2000), nullable=True)
    created_by = Column(String(250), nullable=True)
    created_on = Column(DateTime, nullable=True)
    img_url = Column(String(2000), nullable=True)


# The following class is a representation of DB Table user_details used to
# capture all the logged in users basic info
class User_Details(Base):
    __tablename__ = 'user_details'

    user_email = Column(String(250), primary_key=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=True)
    img = Column(String(2000), nullable=True)


# The following class is a representation of DB table sales_item which
# stores information about all the Cars under every category.
class Sales_Item(Base):
    __tablename__ = 'sales_item'

    item_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(2000), nullable=True)
    price = Column(String(8))
    created_by = Column(String(250), nullable=True)
    created_on = Column(DateTime, nullable=True)
    category_id = Column(Integer, ForeignKey('sales_category.category_id'))
    user_email = Column(String(250), ForeignKey('user_details.user_email'))
    sales_category = relationship(Sales_Category)
    user_details = relationship(User_Details)

# The Following property is set inorder to retreive JSON object of all the
# sales_item available
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
