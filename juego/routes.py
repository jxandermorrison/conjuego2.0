from juego import app, mongo

from flask import render_template, request
from flask import jsonify

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/en")
def english():
    return render_template("game.html")

@app.route("/es")
def spanish():
    return render_template("game.html")

@app.route("/pt")
def portuguese():
    return render_template("game.html")

@app.route("/jp")
def japanese():
    return render_template("game.html")

@app.route("/verbs/<language>")
def verbs(language):
    pipeline = [
        {"$match": {"language": language}},
        {"$sample": {"size": 1}}
    ]
    group = mongo.db.verbs.aggregate(pipeline).next()
    group["_id"] = str(group["_id"])
    
    return jsonify(group)
