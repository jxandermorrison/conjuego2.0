from flask import Flask, request
from flask_pymongo import PyMongo
from flask_babel import Babel
from configuration import Config

app = Flask(__name__)
app.config.from_object(Config)
mongo = PyMongo(app)
babel = Babel(app)

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config["LANGUAGES"])

from juego import routes
