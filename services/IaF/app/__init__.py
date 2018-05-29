from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import controller
from app import database
#from app import datasets