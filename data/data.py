from pymongo import MongoClient
import pandas as pd
from CONFIG import USER, PASSWORD, URL

client = MongoClient("mongodb+srv://{}:{}@{}".format(USER, PASSWORD, URL))

col = client["verbs"]["verbs"]

endf = pd.read_csv("english-final.csv")
esdf = pd.read_csv("spanish-final.csv")
ptdf = pd.read_csv("portuguese-final.csv")
jpdf = pd.read_csv("japanese-final.csv")

full = endf.append(esdf, sort=True).append(ptdf, sort=True).append(jpdf, sort=True)

full = full.loc[:, ~full.columns.str.contains("Unnamed")]

full = full.drop(columns=["pt_tense", "pt_mood", "es_mood", "es_tense"])

full = full.rename(columns={"en_tense": "tense", "en_mood": "mood"})

full.loc[(full["mood"] == "subjunctive") & (full["tense"] == "imperfect"), "tense"] = "imperfect (ra)"
full.loc[(full["mood"] == "subjunctive") & (full["tense"] == "imperfect 2"), "tense"] = "imperfect (se)"

full = full.fillna("")

data = full.to_dict(orient="records")

col.insert_many(data)

client.close()
