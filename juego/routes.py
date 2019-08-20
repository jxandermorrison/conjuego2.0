from juego import app

from flask import render_template

group = {
    "language": "japanese",
    "infinitive": "いる",
    "subject": " - ",
    "answer": "いよう",
    "kana": "いよう",
    "romaji": "iyou",
    "en_mood": "normal",
    "en_tense": "volitional",
    "es_mood": "normal",
    "es_tense": "volitivo",
    "pt_mood": "normal",
    "pt_tense": "volitivo"
}

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/en")
def english():
    return render_template("game.html", group=group)

@app.route("/es")
def spanish():
    return render_template("game.html", group=group)

@app.route("/pt")
def portuguese():
    return render_template("game.html", group=group)

@app.route("/jp")
def japanese():
    return render_template("game.html", group=group)
