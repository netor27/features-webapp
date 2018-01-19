import os
# Configuration file, You need to replace the next values with the appropriate values for your configuration

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
DATABASE_HOST = "127.0.0.1" # For local  use
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}" \
                          .format(DB_USER="apiuser", DB_PASS="password", \
                          DB_ADDR=DATABASE_HOST, DB_NAME="test_features")
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')
PAGINATION_PAGE_SIZE = 5
PAGINATION_PAGE_ARGUMENT_NAME = 'page'
SERVER_NAME = '0.0.0.0:5000'