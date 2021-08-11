# Python script to populate data in itemcatalog db.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Categories, Base, Items, User

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

# Creating db session
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Creating dummy user
User1 = User(name="Nikita Chouhan", email="nikita.ch@gmail.com")
session.add(User1)
session.commit()

# Adding New Catalog Catagories and Items
# Add First Catagory with new items
categories1 = Categories(user_id=1, name="Graphic Novels")

session.add(categories1)
session.commit()

categoryItem1 = Items(user_id=1, name="WatchMen", price="1.50",
                      status="Available",
                      description=('Watchmen is an American comic book '
                                   'series by British creative team of '
                                   'writer Alan Moore, artist Dave Gibbons '
                                   'and colorist John Higgins. '),
                      item_category=categories1)

session.add(categoryItem1)
session.commit()


categoryItem2 = Items(user_id=1, name="Saga Series", price="1.50",
                      status="Available",
                      description=('This book series is written by Brian k.'
                                   'Vaughan and illustrated by'
                                   'Fiona Staples.'),
                      item_category=categories1)

session.add(categoryItem2)
session.commit()

categoryItem3 = Items(user_id=1, name="The Sandman Series", price="1.50",
                      status="Available",
                      description=('The sandman is a comic book series '
                                   'written by Neil Gaiman. '),
                      item_category=categories1)

session.add(categoryItem3)
session.commit()

# Add Second Catagory with new items
categories2 = Categories(user_id=1, name="Historical Fiction")

session.add(categories2)
session.commit()


categoryItem1 = Items(user_id=1, name="The Kite Runner", price="1.50",
                      status="Available",
                      description=('The Kite Runner is written by '
                                   'Khaled Hosseini. '
                                   'It is an unusual and powerful novel that '
                                   'has become a beloved, '
                                   'one-of-a-kind classic. '),
                      item_category=categories2)

session.add(categoryItem1)
session.commit()

categoryItem2 = Items(user_id=1, name="A Gentleman in Moscow", price="1.50",
                      status="Available",
                      description=('From the New York Times bestselling '
                                   'author of Rules of Civility - a'
                                   'transporting novel about a man '
                                   'who is ordered to spend the '
                                   'rest of his life inside a luxury hotel.'),
                      item_category=categories2)

session.add(categoryItem2)
session.commit()

categoryItem3 = Items(user_id=1, name="Catch 22", price="1.50",
                      status="Available",
                      description=('Catch-22 is a satirical war novel '
                                   'by American '
                                   'author Joseph Heller.The book was '
                                   'made into a film adaption in 1970 '
                                   'directed by Mike Nicholas.'),
                      item_category=categories2)

session.add(categoryItem3)
session.commit()

# Add Third Catagory with new items
categories3 = Categories(user_id=1, name="Science Fiction")

session.add(categories3)
session.commit()


categoryItem1 = Items(user_id=1, name="The Hitchhiker's Guide to the Galaxy",
                      price="1.50",
                      status="Available",
                      description=('The Hitchhikers Guide to the Galaxy '
                                   'is a comedy science fiction franchise '
                                   'created by Douglas Adams.'),
                      item_category=categories3)

session.add(categoryItem1)
session.commit()

categoryItem2 = Items(user_id=1, name="1984", price="1.50",
                      status="Available",
                      description=('A dystopian social science fiction novel '
                                   'by English novelist George Orwell.'),
                      item_category=categories3)

session.add(categoryItem2)
session.commit()


print("added catalog items!")
