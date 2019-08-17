import requests
import pandas as pd

df = pd.read_csv("english.csv")

columns = [
    "language",
    "infinitive",
    "subject",
    "answer",
    "jp_mood",
    "jp_tense",
    "pt_mood",
    "pt_tense",
    "es_mood",
    "es_tense",
    "en_mood",
    "en_tense",
]

df["mood"] = df["mood"].str.lower()
df["tense"] = df["tense"].str.lower()

df = df.rename(columns={
    "mood": "es_mood",
    "tense": "es_tense",
})

df["language"] = "english"

df = df.drop(["Unnamed: 0", "translation", "definition"], axis=1)

df["language"] = "english"

df = df.drop(["id"], axis=1)

df.loc[df["es_tense"] == "pasado", "pt_tense"] = "passado"
df.loc[df["es_tense"] == "presente","pt_tense"] = "presente"
df.loc[df["es_tense"] == "futuro","pt_tense"] = "futuro"
df.loc[df["es_tense"] == "afirmativo","pt_tense"] = "afirmativo"
df.loc[df["es_tense"] == "negativo","pt_tense"] = "negativo"

df.loc[df["es_mood"] == "indicativo","pt_mood"] = "indicativo"
df.loc[df["es_mood"] == "perfecto","pt_mood"] = "perfeito"
df.loc[df["es_mood"] == "imperativo","pt_mood"] = "imperativo"
df.loc[df["es_mood"] == "continuo","pt_mood"] = "contínuo"
df.loc[df["es_mood"] == "continuo perfecto","pt_mood"] = "perfeito contínuo"
df.loc[df["es_mood"] == "continuo perfecto","es_mood"] = "perfecto continuo"

df.loc[df["es_tense"] == "pasado", "jp_tense"] = "過去"
df.loc[df["es_tense"] == "presente","jp_tense"] = "現在時制"
df.loc[df["es_tense"] == "futuro","jp_tense"] = "未来"
df.loc[df["es_tense"] == "afirmativo","jp_tense"] = "肯定的な"
df.loc[df["es_tense"] == "negativo","jp_tense"] = "否定の"

df.loc[df["es_mood"] == "indicativo","jp_mood"] = "直説法"
df.loc[df["es_mood"] == "perfecto","jp_mood"] = "完了"
df.loc[df["es_mood"] == "imperativo","jp_mood"] = "命令的な"
df.loc[df["es_mood"] == "continuo","jp_mood"] = "連続"
df.loc[df["es_mood"] == "continuo perfecto","jp_mood"] = "連続完了"

df.loc[df["es_tense"] == "pasado", "en_tense"] = "past"
df.loc[df["es_tense"] == "presente","en_tense"] = "present"
df.loc[df["es_tense"] == "futuro","en_tense"] = "future"
df.loc[df["es_tense"] == "afirmativo","en_tense"] = "affirmativeな"
df.loc[df["es_tense"] == "negativo","en_tense"] = "negativeの"

df.loc[df["es_mood"] == "indicativo","en_mood"] = "indicative"
df.loc[df["es_mood"] == "perfecto","en_mood"] = "perfect"
df.loc[df["es_mood"] == "imperativo","en_mood"] = "imperativeな"
df.loc[df["es_mood"] == "continuo","en_mood"] = "continuous"
df.loc[df["es_mood"] == "continuo perfecto","en_mood"] = "perfect continuous"

df = df[columns]


df.to_csv("english-final.csv")
