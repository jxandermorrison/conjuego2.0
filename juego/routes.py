from juego import app, mongo

from flask import render_template, request
from flask import jsonify
from flask_babel import _

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/en")
def english():

    subjects = mongo.db.verbs.find({"language": "english"}).distinct("subject")
    moods = mongo.db.verbs.find({"language": "english"}).distinct("mood")
    tenses = mongo.db.verbs.find({"language": "english"}).distinct("tense")

    return render_template("game.html", moods=moods, tenses=tenses, subjects=subjects)

@app.route("/es")
def spanish():

    subjects = mongo.db.verbs.find({"language": "spanish"}).distinct("subject")
    moods = mongo.db.verbs.find({"language": "spanish"}).distinct("mood")
    tenses = mongo.db.verbs.find({"language": "spanish"}).distinct("tense")

    return render_template("game.html", moods=moods, tenses=tenses, subjects=subjects)

@app.route("/pt")
def portuguese():

    subjects = mongo.db.verbs.find({"language": "portuguese"}).distinct("subject")
    moods = mongo.db.verbs.find({"language": "portuguese"}).distinct("mood")
    tenses = mongo.db.verbs.find({"language": "portuguese"}).distinct("tense")

    return render_template("game.html", moods=moods, tenses=tenses, subjects=subjects)

@app.route("/jp")
def japanese():

    moods = mongo.db.verbs.find({"language": "japanese"}).distinct("mood")
    tenses = mongo.db.verbs.find({"language": "japanese"}).distinct("tense")

    return render_template("game.html", moods=moods, tenses=tenses)

@app.route("/verbs/<language>")
def verbs(language):
    pipeline = [
        {"$match": {"language": language}},
        {"$sample": {"size": 1}}
    ]
    group = mongo.db.verbs.aggregate(pipeline).next()
    group["_id"] = str(group["_id"])
    
    return jsonify(group)
