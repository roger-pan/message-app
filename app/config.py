import os


class Config(object):

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '12345'
    
    pw = os.environ.get('POSTGRESPW')
    user = os.environ.get('PGUSER', 'postgres')
    url = os.environ.get('PGHOST', 'localhost')
    db = os.environ.get('PGDATABASE', 'messenger')    
    # postgres
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{pw}@{url}/{db}'

    # Flask-User configuration
    # USER_APP_NAME = "Flasky To-Do App"      # Shown in and email templates and page footers
    # USER_ENABLE_EMAIL = False      # Disable email authentication
    # USER_ENABLE_USERNAME = True    # Enable username authentication
    # USER_REQUIRE_RETYPE_PASSWORD = False    # Simplify register form


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True