import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    """Base Config Object"""
    DEBUG = os.environ.get('FLASK_DEBUG', False)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a76562a5b33ecbd199be08cdb4443a02e26bd2c3c')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:Chamo.Pzo@localhost:5432/users_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # This is just here to suppress a warning from SQLAlchemy as it will soon be removed