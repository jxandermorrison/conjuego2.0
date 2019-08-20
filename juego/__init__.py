from flask import Flask
from flask_pymongo import PyMongo
from CONFIG import USER, PASSWORD, URL

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://{}:{}@{}".format(USER, PASSWORD, URL)
mongo = PyMongo(app)

from juego import routes
