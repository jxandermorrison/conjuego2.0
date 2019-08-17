import requests
import sys
from bs4 import BeautifulSoup
import pandas as pd

df = pd.DataFrame([], columns=[
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
])

verbs = pd.read_csv("portuguese.csv")

url = "https://www.conjugateverb.com/pt/{}"

verb_list = verbs["Verb"]

full_subjects = [
    ["eu"], 
    ["tu"], 
    ["ele", "ela", "você"], 
    ["nós"], 
    ["vós"], 
    ["eles", "elas", "vocês"]
]

more = {
    "present_continuous": ["estou", "estás", "está", "estamos", "estais", "estão"],
    "preterite_continuous": ["estive", "estiveste", "esteve", "estivemos", "estivestes", "estiveram"],
    "imperfect_continuous": ["estava", "estavas", "estava", "estávamos", "estáveis", "estavam"],
    "conditional_continuous": ["estaria", "estarias", "estaria", "estaríamos", "estaríeis", "estariam"],
    "future_continuous": ["estarei", "estarás", "estará", "estaremos", "estareis", "estarão"],

    "present_perfect": ["tenho", "tens", "tem", "temos", "tendes", "têm"],
    "past_perfect": ["tinha", "tinhas", "tinha", "tínhamos", "tínheis", "tinham"],
    "future_perfect": ["terei", "terás", "terá", "teremos", "tereis", "terão"],
    "conditional_perfect": ["teria", "terias", "teria", "teríamos", "teríeis", "teriam"]
}

verb_length_list = len(verb_list)
counter = 1

for verb in verb_list:
    print(counter, "of", verb_length_list)
    counter += 1

    verb = verb.strip("[")
    verb = verb.strip("]")

    page = requests.get(url.format(verb))

    soup = BeautifulSoup(page.text, "html.parser")

    tables = soup.find_all("table", {"class": ["x", "y", "z"]})
    participles = soup.find("div", {"class": "c"})

    try:
        kinds = [i.get_text() for i in participles.find_all("th")]
    except:
        continue
    forms = [j.get_text() for j in participles.find_all("td")]

    participles = dict(zip(kinds, forms))

    for table in tables:

        title = table["title"][:-11].lower().strip()
        if title in ["affirmative", "negative"]:
            mood = "imperative"
            tense = title
        elif title in ["conditional", "personal infinitive"]:
            mood = "indicative"
            tense = title
        else:
            index = title.rfind(" ")
            tense = title[:index]
            mood = title[index + 1:]

        if "pluperfect" in tense:
            mood = "perfect"
            tense = "past"

        if "imperfect" in tense:
            tense = "imperfect"

        for i, item in enumerate(table.find_all("td")):
            full_text = item.get_text()
            full_text = full_text.strip()

            if full_text == "":
                continue

            helpers = item.find_all("i")

            subject = helpers[-1].get_text().strip()
            peripherals = " ".join([helper.get_text() for helper in helpers[:-1]]).strip()

            conjugation = item.find(text=True, recursive=False).strip()

            if mood == "continuous (progressive)":
                mood = "continuous"

            if tense == "present":
                es_tense = "presente"
                pt_tense = "presente"
            elif tense == "preterite":
                es_tense = "pretérito"
                pt_tense = "pretérito"
            elif tense == "imperfect" or tense == "imperfect 2":
                es_tense = "imperfecto"
                pt_tense = "imperfeito"
            elif tense == "conditional":
                es_tense = "condicional"
                pt_tense = "condicional"
            elif tense == "future":
                es_tense = "futuro"
                pt_tense = "futuro"
            elif tense == "past":
                es_tense = "pasado"
                pt_tense = "pasado"
            elif tense == "affirmative":
                es_tense = "afirmativo"
                pt_tense = "afirmativo"
            elif tense == "negative":
                es_tense = "negativo"
                pt_tense = "negativo"
            elif tense == "personal infinitive":
                es_tense = "infinitivo personal"
                pt_tense = "infinitivo pessoal"
            else:
                raise ValueError

            if mood == "indicative":
                es_mood = "indicativo"
                pt_mood = "indicativo"
            elif mood == "subjunctive":
                es_mood = "subjuntivo"
                pt_mood = "subjuntivo"
            elif mood == "imperative":
                es_mood = "imperativo"
                pt_mood = "imperativo"
            elif mood == "continuous":
                es_mood = "continuo"
                pt_mood = "contínuo"
            elif mood == "perfect":
                es_mood = "perfecto"
                pt_mood = "perfeito"
            elif mood == "perfect subjunctive":
                es_mood = "subjuntivo perfecto"
                pt_mood = "subjuntivo perfeito"
            else:
                raise ValueError


            if "ele" == subject:

                for pronoun in ["ele", "ela", "você"]:
                    full_row = {
                        "language": "portuguese",
                        "infinitive": verb,
                        "subject": pronoun,
                        "answer": conjugation,
                        "jp_mood": "",
                        "jp_tense": "",
                        "pt_mood": pt_mood,
                        "pt_tense": pt_tense,
                        "es_mood": es_mood,
                        "es_tense": es_tense,
                        "en_mood": mood,
                        "en_tense": tense,
                    }

                    df = df.append(full_row, ignore_index=True)

            elif "eles" == subject:

                for pronoun in ["eles", "elas", "vocês"]:
                    full_row = {
                        "language": "portuguese",
                        "infinitive": verb,
                        "subject": pronoun,
                        "answer": conjugation,
                        "jp_mood": "",
                        "jp_tense": "",
                        "pt_mood": pt_mood,
                        "pt_tense": pt_tense,
                        "es_mood": es_mood,
                        "es_tense": es_tense,
                        "en_mood": mood,
                        "en_tense": tense,
                    }

                    df = df.append(full_row, ignore_index=True)

            else:

                full_row = {
                    "language": "portuguese",
                    "infinitive": verb,
                    "subject": subject,
                    "answer": conjugation,
                    "jp_mood": "",
                    "jp_tense": "",
                    "pt_mood": pt_mood,
                    "pt_tense": pt_tense,
                    "es_mood": es_mood,
                    "es_tense": es_tense,
                    "en_mood": mood,
                    "en_tense": tense,
                }
                df = df.append(full_row, ignore_index=True)


    for tense_mood in more:
        j = tense_mood.find("_")
        tense = tense_mood[:j]
        mood = tense_mood[j + 1:]

        for k in range(len(full_subjects)):
            pronouns = full_subjects[k]
            if mood == "perfect":
                add_part = participles["past"]
            elif mood == "continuous":
                add_part = participles["present"]
            conjugation = " ".join([more[tense_mood][k], add_part])

            for pronoun in pronouns:

                if tense == "present":
                    es_tense = "presente"
                    pt_tense = "presente"
                elif tense == "preterite":
                    es_tense = "pretérito"
                    pt_tense = "pretérito"
                elif tense == "imperfect" or tense == "imperfect 2":
                    es_tense = "imperfecto"
                    pt_tense = "imperfeito"
                elif tense == "conditional":
                    es_tense = "condicional"
                    pt_tense = "condicional"
                elif tense == "future":
                    es_tense = "futuro"
                    pt_tense = "futuro"
                elif tense == "past":
                    es_tense = "pasado"
                    pt_tense = "pasado"
                elif tense == "affirmative":
                    es_tense = "afirmativo"
                    pt_tense = "afirmativo"
                elif tense == "negative":
                    es_tense = "negativo"
                    pt_tense = "negativo"
                elif tense == "personal infinitive":
                    es_tense = "infinitivo personal"
                    pt_tense = "infinitivo pessoal"
                else:
                    raise ValueError

                if mood == "indicative":
                    es_mood = "indicativo"
                    pt_mood = "indicativo"
                elif mood == "subjunctive":
                    es_mood = "subjuntivo"
                    pt_mood = "subjuntivo"
                elif mood == "imperative":
                    es_mood = "imperativo"
                    pt_mood = "imperativo"
                elif mood == "continuous":
                    es_mood = "continuo"
                    pt_mood = "contínuo"
                elif mood == "perfect":
                    es_mood = "perfecto"
                    pt_mood = "perfeito"
                elif mood == "perfect subjunctive":
                    es_mood = "subjuntivo perfecto"
                    pt_mood = "subjuntivo perfeito"
                else:
                    raise ValueError

                full_row = {
                    "language": "portuguese",
                    "infinitive": verb,
                    "subject": pronoun,
                    "answer": conjugation,
                    "jp_mood": "",
                    "jp_tense": "",
                    "pt_mood": pt_mood,
                    "pt_tense": pt_tense,
                    "es_mood": es_mood,
                    "es_tense": es_tense,
                    "en_mood": mood,
                    "en_tense": tense,
                }
                df = df.append(full_row, ignore_index=True)

df.to_csv("portuguese-final.csv")
