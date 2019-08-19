import pandas as pd
import sys

df = pd.read_csv("japanese.csv")

df["subject"] = ""

df.loc[df["en_tense"] == "present", "es_tense"] = "presente"
df.loc[df["en_tense"] == "present", "pt_tense"] = "presente"

df.loc[df["en_tense"] == "negative", "es_tense"] = "negativo"
df.loc[df["en_tense"] == "negative", "pt_tense"] = "negativo"

df.loc[df["en_tense"] == "past", "es_tense"] = "pasado"
df.loc[df["en_tense"] == "past", "pt_tense"] = "passado"

df.loc[df["en_tense"] == "past negative", "es_tense"] = "pasado negativo"
df.loc[df["en_tense"] == "past negative", "pt_tense"] = "passado negativo"

df.loc[df["en_tense"] == "te form", "es_tense"] = "て (te)"
df.loc[df["en_tense"] == "te form", "pt_tense"] = "て (te)"
df.loc[df["en_tense"] == "te form", "en_tense"] = "て (te)"

df.loc[df["en_tense"] == "tai form", "es_tense"] = "たい (tai)"
df.loc[df["en_tense"] == "tai form", "pt_tense"] = "たい (tai)"
df.loc[df["en_tense"] == "tai form", "en_tense"] = "たい (tai)"

df.loc[df["en_tense"] == "volitional", "es_tense"] = "volitivo"
df.loc[df["en_tense"] == "volitional", "pt_tense"] = "volitivo"

df.loc[df["en_tense"] == "imperative", "es_tense"] = "imperativo"
df.loc[df["en_tense"] == "imperative", "pt_tense"] = "imperativo"

df.loc[df["en_tense"] == "passive", "es_tense"] = "pasivo"
df.loc[df["en_tense"] == "passive", "pt_tense"] = "passivo"

df.loc[df["en_tense"] == "conditional", "es_tense"] = "condicional"
df.loc[df["en_tense"] == "conditional", "pt_tense"] = "condicional"

df.loc[df["en_tense"] == "provisional conditional", "es_tense"] = "condicional provisional"
df.loc[df["en_tense"] == "provisional conditional", "pt_tense"] = "condicional provisional"

df.loc[df["en_tense"] == "causative", "es_tense"] = "causativo"
df.loc[df["en_tense"] == "causative", "pt_tense"] = "condicional"

df.loc[df["en_tense"] == "potential", "es_tense"] = "potencial"
df.loc[df["en_tense"] == "potential", "pt_tense"] = "potencial"

df.loc[df["en_mood"] == "plain", "en_mood"] = "normal"
df.loc[df["en_mood"] == "normal", "es_mood"] = "normal"
df.loc[df["en_mood"] == "normal", "pt_mood"] = "normal"

df.loc[df["en_mood"] == "keigo (polite)", "en_mood"] = "polite"
df.loc[df["en_mood"] == "polite", "es_mood"] = "educado"
df.loc[df["en_mood"] == "polite", "pt_mood"] = "educado"

df.to_csv("japanese-final.csv")
