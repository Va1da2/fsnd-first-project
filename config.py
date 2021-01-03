import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgres://vaidas@localhost:5432/fyyur'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Provide env variables to not set thom always though CLI
FLASK_APP = "fsnd-first-project"
FLASK_ENV = "development"