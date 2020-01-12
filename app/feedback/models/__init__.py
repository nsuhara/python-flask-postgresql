"""app/feedback/models/__init__.py
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init():
    """init
    """
    db.create_all()
