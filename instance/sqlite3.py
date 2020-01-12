"""instance/sqlite3.py
"""

import os

SQLALCHEMY_DATABASE_URI = 'sqlite:///{host}/{name}'.format(**{
    'host': os.path.dirname(os.path.abspath(__file__)),
    'name': 'db.sqlite3'
})
