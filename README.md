# Glass Force Wiki
Made with Flask and PostgreSQL

### api.py
Creates the Flask app object as well as the objects for the Flask features packages.

- SQLAlchemy for accessing the database
- Flask-Migrate for Flask support for Alembic. 
- LoginManager for user login state.

### Routes.py
TODO: Separate player_characters from characters

### Models.py
#### User:
- User['password_hash'] means the password won't be stored as plain text.
- User['posts'] is the relationship between a user and the Entrys they have authored.
#### Character:
#### Entry:
- Entry['timestamp'] is passed the function datetime.utcnow instead of a call utcnow(). It needs to be converted to a user's local time.
- Get an expression defined by backref='author' in the User class to reference the object tied to an entry's user_id foreign key.

### forms.py
#### RegistrationForm
- Uses validator *Email()* to check that given input is in email format.
- Uses validator *EqualTo()* to check that the field is the same as the first field (as is standard for password creation).

## Packages:
*SQLAlchemy/Flask-SQLAlchemy*: Object Relational Mapper for managing the database without SQL. Instead, using classes and methods.

*Alembic/Flask-Migrate*: used as a database migration framework for SQLAlchemy for upgrading/downgrading the database.