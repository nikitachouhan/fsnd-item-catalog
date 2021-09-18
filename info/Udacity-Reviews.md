# Project Review

- [Review](#review)
- [Suggestions](#suggestions)


## Review

### Meets Specifications

Congratulations! :tada: :tada:
Amazing effort, you've created a great project, well organized, and nice documented.

Your project doesn't meet specifications, It exceeds it! :smile:

Be proud of yourself, you're a great developer. :surfer:

### API Endpoints

The project implements a JSON endpoint that serves the same information as displayed in the HTML endpoints for an arbitrary item in the catalog.

Great job, Try to make usage of your JSON endpoint using json.load(). Please refer to documentation [here](https://docs.python.org/3/library/json.html).

### CRUD: Read

Website reads category and item information from a database.

All Category and Item information are read from the database with a well formatted structure.

### CRUD: Create

Website includes a form allowing users to add new items and correctly processes submitted forms.

Nice work, all category and item information are stored in the database.

### CRUD: Update

Website does include a form to edit/update a current record in the database table and correctly processes submitted forms.

Excellent work I can successfully update items.

- Please consider to have the ON DELETE CASCADE functionality implemented to ensure database's integrity, please look at the code review section about how to do the implementation.
- It would be better for all the POST request, you could include the csrf_token, [flask-seasurf](https://flask-seasurf.readthedocs.io/en/latest/) provides you some simple way for this improvement.

### CRUD: Delete

Website does include a function to delete a current record.

Great job!

If you eventually allow users to manage categories you will need to deal with orphaned rows in your database. When deleting a parent row (category) you need to delete all child rows (items) associated with it. Please see SQLAlchemy [documentaion](http://docs.sqlalchemy.org/en/latest/orm/cascades.html) on cascades.

### Authentication & Authorization

Create, delete and update operations do consider authorization status prior to execution.

Authorization works as expected.

Page implements a third-party authentication & authorization service (like Google Accounts or Mozilla Persona) instead of implementing its own authentication & authorization spec.

You successfully implemented a Google OAuth Service. Well done.

Make sure there is a 'Login' and 'Logout' button/link in the project. The aesthetics of this button/link is up to the discretion of the student.

The aesthetics of the Login and Logout link in your project, is well implemented.

### Code Quality

Code is ready for personal review and neatly formatted and compliant with the Python [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide.

Well done, your code is PEP8 compliant.

### Comments

Comments are present and effectively explain longer code procedures.

Remember that there are always three places where you should write concise comments:

- Header comment
  You should write at least what the code should do. You can also write your name, the date and why you wrote the code

- Function Header
  This comment should provide information about the purpose of the function. You should include at least the required parameters (if any), the transformations, and the expected output

- Inline (above line) comment
  You should write this type of comment in any part of your code you feel that no everyone will get what you are trying to achieve with certain the function or partial code.

In term of comments style, you can use Pycco or DocString.

Finally, if you may require some inspiration or advice about what or how to write better comments, you can check the following blog post: http://www.hongkiat.com/blog/source-code-comment-styling-tips/

References
http://www.cs.utah.edu/~germain/PPS/Topics/commenting.html

### Documentation

README file includes details of all the steps required to successfully run the application.

Great Job! Readme file includes details about how to set up the database and run your project.

## Suggestions

1.  populate_db_data.py

```python
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
```

Right now there is a lot code repetition in order to add your test data, which increases the chance of an error while writing to your DB. It's also not very convenient to do for many DB items, even if you wanted to randomly generate test data or fetch it from online data.
Python comes with powerful packages/module like json, csv.

Why not store your test data in a suitable data model, such as a JSON, and iterate through it with a method.
the great advantage of doing it this way, is that the code that actually touches your DB is only written once, you could easily write random test data to fill it to make it as large as you need with no extra work, or you can fill it with sample data from online sites. You could of course also export and import it via a JSON file.
An example code (with different database schema):

```python
category_json = json.loads("""{
"all_categories": [
  {
    "created_date": null,
    "id": 29,
    "name": "Books",
    "no_of_visits": 1
  },
  {
    "created_date": null,
    "id": 21,
    "name": "Camping",
    "no_of_visits": 7
  },
  {
    "created_date": null,
    "id": 20,
    "name": "Kitchenware",
    "no_of_visits": 1
  },
  {
    "created_date": null,
    "id": 32,
    "name": "Laptops",
    "no_of_visits": 10
  },

  {
    "created_date": null,
    "id": 31,
    "name": "Susan's Moving Items",
    "no_of_visits": 8
  }
]
}""")

for e in category_json['all_categories']:
category_input = Category(
  name=str(e['name']),
  id=str(e['id']),
  no_of_visits=0,
  user_id=1
  )
session.add(category_input)
session.commit()
```

2.  app.py

```python
app.route('/<category>/<item>/edit',
           methods=['GET', 'POST'])
def editItem(category, item):
    # check user login state
    user_login = None
    if 'username' in login_session:
        user_login = True
    else:
        flash('Login required to update item.')
        return redirect(url_for('homePage'))

    if request.method == 'POST':
        # fetch item category
        category = session.query(Categories).filter_by(
            name=category).one()
        # fetch item to edit
        item = session.query(Items).filter_by(
            name=item, item_category_id=category.id).one()
```

It's better to use .one_or_none() instead of .one(); as .one() raises sqlalchemy.orm.exc.NoResultFound if the query selects no rows. While .one_or_none() returns None if the query selects no rows.

With no rows found using .one(), E.g:

```sh
>>> user = query.filter(User.id == 99).one()
Traceback (most recent call last):
...
NoResultFound: No row was found for one()
```

With no rows found using .one_or_none(), E.g:

```sh
>>> user = query.filter(User.id == 99).one_or_none()
<<< None
```

Reference:
http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.one_or_none
.one_or_none() is like .one(), except that if no results are found, it doesn’t raise an error; it just returns None. Like .one(), however, it does raise an error if multiple results are found.
