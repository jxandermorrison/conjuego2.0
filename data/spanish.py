import requests
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

verbs = pd.read_csv("spanish.csv")

url = "https://www.spanishdict.com/conjugate/{}"

verb_list = verbs["Verb"]
y = 0

for verb in verb_list:
    y += 1
    print(y, "of", len(verb_list))
    page = requests.get(url.format(verb))
    soup = BeautifulSoup(page.text, "html.parser")

    defs = soup.find_all("div", {"class": "quickdefWrapper--HELyO"})
    infinitive = soup.find("div", {"class": "headwordDesktop--2XpdH"}).get_text()

    quick_defs = []

    for d in defs:
        quick_defs.append(d.get_text())

    definitions = ", ".join(quick_defs)

    vtable_headers = soup.find_all("div", {"class": "vtable-header"})
    for vtable_header in vtable_headers:
        child = list(vtable_header.children).pop(0)

        span = child.find("span", {"class": "vtable-label-link-text"})
        mood = span.get_text()

        vtable_wrapper = vtable_header.next_sibling

        header_row = vtable_wrapper.find("tr", {"class": "vtable-head-row"})

        tenses = [i.get_text() for i in header_row.find_all("td", {"class": "vtable-title"})]

        body_rows = vtable_wrapper.find_all("tr", {"class": "vtable-body-row"})

        for body_row in body_rows:
            subject = body_row.find("td", {"class": "vtable-pronoun"}).get_text()

            conjugations = body_row.find_all("td", {"class": "vtable-word"})

            for i, conjugation in enumerate(conjugations):
                verb = conjugation.get_text()
                tense = tenses[i]

                mood = mood.lower()
                tense = tense.lower()
                definitions = definitions.lower()

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

                if mood == "indicative":
                    es_mood = "indicativo"
                    pt_mood = "indicativo"
                if mood == "subjunctive":
                    es_mood = "subjuntivo"
                    pt_mood = "subjuntivo"
                if mood == "imperative":
                    es_mood = "imperativo"
                    pt_mood = "imperativo"
                if mood == "continuous":
                    es_mood = "continuo"
                    pt_mood = "contínuo"
                if mood == "perfect":
                    es_mood = "perfecto"
                    pt_mood = "perfeito"
                if mood == "perfect subjunctive":
                    es_mood = "subjuntivo perfecto"
                    pt_mood = "subjuntivo perfeito"

                if "/" in subject:

                    subjects = subject.split("/")

                    for pronoun in subjects:
                        full_row = {
                            "language": "spanish",
                            "infinitive": infinitive,
                            "subject": pronoun,
                            "answer": verb,
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
                        "language": "spanish",
                        "infinitive": infinitive,
                        "subject": subject,
                        "answer": verb,
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

df.to_csv("spanish-final.csv")
