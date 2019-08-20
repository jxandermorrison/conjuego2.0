from juego import app, mongo

from flask import render_template

google_translate = "https://translate.google.com/#view=home&op=translate&sl={}&tl={}&text={}"

en_pipeline = [
    {"$match": {"language": "english"}},
    {"$sample": {"size": 1}}
]

es_pipeline = [
    {"$match": {"language": "spanish"}},
    {"$sample": {"size": 1}}
]

pt_pipeline = [
    {"$match": {"language": "portuguese"}},
    {"$sample": {"size": 1}}
]

jp_pipeline = [
    {"$match": {"language": "japanese"}},
    {"$sample": {"size": 1}}
]

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/en")
def english():
    group = mongo.db.verbs.aggregate(en_pipeline).next()

    return render_template("game.html")

@app.route("/es")
def spanish():
    group = mongo.db.verbs.aggregate(es_pipeline).next()

    return render_template("game.html")

@app.route("/pt")
def portuguese():
    group = mongo.db.verbs.aggregate(pt_pipeline).next()

    return render_template("game.html")

@app.route("/jp")
def japanese():
    group = mongo.db.verbs.aggregate(jp_pipeline).next()
    
    return render_template("game.html", group=group)
