import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    ROOT_DIR = os.path.dirname(__file__)
    # DATA_DIR = os.path.join(ROOT_DIR, 'data')
    # DATABASE_DIR = os.path.join(ROOT_DIR, 'db')
    # SCRAPING_DIR = os.path.join(ROOT_DIR, 'scraping')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + ROOT_DIR + '/got.db'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False