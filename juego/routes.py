from juego import app, mongo
import json
from urllib.parse import unquote

from flask import render_template, request
from flask import jsonify
from flask_babel import _

languages = ["en", "es", "pt"]

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/en")
def english():

    subjects = mongo.db.verbs.find({"language": "english"}).distinct("subject")
    lang = request.accept_languages.best_match(languages) or "en"
    moods = mongo.db.verbs.find({"language": "english"}).distinct(lang + "_mood")
    tenses = mongo.db.verbs.find({"language": "english"}).distinct(lang + "_tense")

    return render_template("game.html", moods=moods, tenses=tenses, subjects=subjects, title=_("English"))

@app.route("/es")
def spanish():

    subjects = mongo.db.verbs.find({"language": "spanish"}).distinct("subject")
    lang = request.accept_languages.best_match(languages) or "en"
    moods = mongo.db.verbs.find({"language": "spanish"}).distinct(lang + "_mood")
    tenses = mongo.db.verbs.find({"language": "spanish"}).distinct(lang + "_tense")

    return render_template("game.html", moods=moods, tenses=tenses, subjects=subjects, title=_("Spanish"))

@app.route("/pt")
def portuguese():

    subjects = mongo.db.verbs.find({"language": "portuguese"}).distinct("subject")
    lang = request.accept_languages.best_match(languages) or "en"
    moods = mongo.db.verbs.find({"language": "portuguese"}).distinct(lang + "_mood")
    tenses = mongo.db.verbs.find({"language": "portuguese"}).distinct(lang + "_tense")

    return render_template("game.html", moods=moods, tenses=tenses, subjects=subjects, title=_("Portuguese"))

@app.route("/jp")
def japanese():

    lang = request.accept_languages.best_match(languages) or "en"
    moods = mongo.db.verbs.find({"language": "japanese"}).distinct(lang + "_mood")
    tenses = mongo.db.verbs.find({"language": "japanese"}).distinct(lang + "_tense")

    return render_template("game.html", moods=moods, tenses=tenses, title=_("Japanese"))

@app.route("/verbs/<language>")
def verbs(language):
    options = json.loads(unquote(request.query_string.decode("utf8")))
    lang = request.accept_languages.best_match(languages) or "en"

    pipeline = [
        {"$match": {"$and": [{"language": language}]}},
        {"$sample": {"size": 1}}
    ]

    for option in options:
        if language == "japanese" and option == "subject":
            continue
        if option in ["mood", "tense"]:
            mod_option = "{}_{}".format(lang, option)
            pipeline[0]["$match"]["$and"].append({mod_option: {"$in": options[option]}})
        else:
            pipeline[0]["$match"]["$and"].append({option: {"$in": options[option]}})

    try:
        group = mongo.db.verbs.aggregate(pipeline).next()
    except:
        return {"language": "None"}
    
    group["_id"] = str(group["_id"])
    group["browser_language"] = lang
    
    return jsonify(group)
