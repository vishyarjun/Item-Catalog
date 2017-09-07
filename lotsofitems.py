#!/usr/bin/python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Sales_Category, Base, Sales_Item

engine = create_engine('sqlite:///salescatalog.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()

session = DBSession()

# Menu for UrbanBurger

category1 = Sales_Category(name='SUZUKI', description='Suzuki',
                           created_by='viswanathan.arjun@gmail.com')
session.add(category1)
session.commit()
category2 = Sales_Category(name='PSA', description='Groupe PSA',
                           created_by='viswanathan.arjun@gmail.com')
session.add(category2)
session.commit()
category3 = Sales_Category(name='FCA', description='FCA',
                           created_by='viswanathan.arjun@gmail.com')
session.add(category3)
session.commit()
category4 = Sales_Category(name='HONDA', description='Honda',
                           created_by='viswanathan.arjun@gmail.com')
session.add(category4)
session.commit()
category5 = Sales_Category(name='FORD', description='Ford',
                           created_by='viswanathan.arjun@gmail.com')
session.add(category5)
session.commit()
category6 = Sales_Category(name='GM', description='General Motors',
                           created_by='viswanathan.arjun@gmail.com')
session.add(category6)
session.commit()

Sales_Item2 = Sales_Item(name='Maruti Suzuki Dzire',
                         description='Maruti Suzuki Dzire',
                         price='$7650', sales_category=category1,
                         created_by='viswanathan.arjun@gmail.com')

session.add(Sales_Item2)
session.commit()

Sales_Item1 = Sales_Item(name='Maruti Suzuki Baleno',
                         description='Maruti Suzuki Baleno',
                         price='$2899', sales_category=category1,
                         created_by='viswanathan.arjun@gmail.com')

session.add(Sales_Item1)
session.commit()

Sales_Item2 = Sales_Item(name='Maruti Suzuki Vitara Brezza',
                         description='Maruti Suzuki Vitara Brezza',
                         price='$5650', sales_category=category1,
                         created_by='viswanathan.arjun@gmail.com')

session.add(Sales_Item2)
session.commit()

Sales_Item3 = Sales_Item(name='Maruti Suzuki Swift',
                         description='Maruti Suzuki Swift',
                         price='$3799', sales_category=category1,
                         created_by='viswanathan.arjun@gmail.com')

session.add(Sales_Item3)
session.commit()

Sales_Item4 = Sales_Item(name='Maruti Suzuki Ertiga',
                         description='Made with grade A beef',
                         price='$7899', sales_category=category1,
                         created_by='viswanathan.arjun@gmail.com')

session.add(Sales_Item4)
session.commit()

Sales_Item5 = Sales_Item(name='Peugeot 3008 II',
                         description='Peugeot 3008 II', price='$1993',
                         sales_category=category2,
                         created_by='viswanathan.arjun@gmail.com')

session.add(Sales_Item5)
session.commit()

Sales_Item6 = Sales_Item(name='Peugeot 308', description='Peugeot 308',
                         price='$3499', sales_category=category2,
                         created_by='viswanathan.arjun@gmail.com')

session.add(Sales_Item6)
session.commit()

Sales_Item7 = Sales_Item(name='Peugeot 307', description='Peugeot 307',
                         price='$3495$', sales_category=category2,
                         created_by='viswanathan.arjun@gmail.com')

session.add(Sales_Item7)
session.commit()

Sales_Item8 = Sales_Item(name='Citroen CX.', description='Citroen CX.',
                         price='$5099$', sales_category=category2,
                         created_by='viswanathan.arjun@gmail.com')

session.add(Sales_Item8)
session.commit()

Sales_Item1 = Sales_Item(name='Citroen GS.', description='Citroen GS.',
                         price='$7996$', sales_category=category2,
                         created_by='viswanathan.arjun@gmail.com')

session.add(Sales_Item1)
session.commit()

Sales_Item2 = Sales_Item(name='Alfa Romeo.', description='Alfa Romeo.',
                         price='$2567$', sales_category=category3,
                         created_by='viswanathan.arjun@gmail.com')

session.add(Sales_Item2)
session.commit()

Sales_Item3 = Sales_Item(name='Dodge.', description='Dodge.',
                         price='1599$', sales_category=category3,
                         created_by='viswanathan.arjun@gmail.com')

session.add(Sales_Item3)
session.commit()

Sales_Item4 = Sales_Item(name='Fiat.', description='Fiat.',
                         price='1276$', sales_category=category3,
                         created_by='viswanathan.arjun@gmail.com')

session.add(Sales_Item4)
session.commit()

Sales_Item5 = Sales_Item(name='Maserati.', description='Maserati.',
                         price='1489$', sales_category=category3,
                         created_by='viswanathan.arjun@gmail.com')

session.add(Sales_Item5)
session.commit()

Sales_Item6 = Sales_Item(name='Jeep.', description='Jeep.',
                         price='1200$', sales_category=category3,
                         created_by='viswanathan.arjun@gmail.com')

session.add(Sales_Item6)
session.commit()
print 'added menu items!'
