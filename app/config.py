"""app/config.py
"""

import os

DEBUG = False
SECRET_KEY = os.getenv('SECRET_KEY', '')
STRIPE_API_KEY = os.getenv('STRIPE_API_KEY', '')

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', '')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
