from juego import app

from flask import render_template

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/en")
def english():
    group = {
        "subject": "I",
        "verb": "think",
        "definition": "pensar",
        "tense": "present",
        "mood": "indicative"
    }
    return render_template("game.html", group=group)

@app.route("/es")
def spanish():
    group = {
        "subject": "I",
        "verb": "think",
        "definition": "pensar",
        "tense": "present",
        "mood": "indicative"
    }
    return render_template("game.html", group=group)

@app.route("/pt")
def portuguese():
    group = {
        "subject": "I",
        "verb": "think",
        "definition": "pensar",
        "tense": "present",
        "mood": "indicative"
    }
    return render_template("game.html", group=group)
