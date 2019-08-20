from pymongo import MongoClient
import pandas as pd

client = MongoClient()

col = client["verbs"]["verbs"]

endf = pd.read_csv("english-final.csv")
esdf = pd.read_csv("spanish-final.csv")
ptdf = pd.read_csv("portuguese-final.csv")
jpdf = pd.read_csv("japanese-final.csv")

full = endf.append(esdf, sort=True).append(ptdf, sort=True).append(jpdf, sort=True)

full = full.loc[:, ~full.columns.str.contains("Unnamed")]

full = full.fillna("")

data = full.to_dict(orient="records")

col.insert_many(data)

client.close()
