# Glass Force Wiki
Made with Flask

### Models.py
#### User:
- User['password_hash'] means the password won't be stored as plain text.
- User['posts'] is the relationship between a user and the Entrys they have authored.
#### Character:
#### Entry:
- Entry['timestamp'] is passed the function datetime.utcnow instead of a call utcnow(). It needs to be converted to a user's local time.
