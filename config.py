"""ENV configs module"""
import os

class Base(object):
    """Parent configuration class."""
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:\\Users\\KK\\Documents\\python\\api\\todo.db'
    SECRET_KEY = '0987654321'
    DEBUG = True


class Development(Base):
    """Development configurations."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:28248477@localhost/flask_api'
    SECRET_KEY = os.getenv('SECRET')



class Testing(Base):
    """Configurations for Testing."""
    TESTING = True
    DEBUG = False
   # DATABASE = os.getenv('TEST_DATABASE')


class Production(Base):
    """Configurations for Production."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    DB_USERNAME = os.getenv('USERNAME')
    DB_PASSWORD = os.getenv('PASSWORD')
    HOST = os.getenv('HOST')
    SECRET_KEY = os.getenv('SECRET')




