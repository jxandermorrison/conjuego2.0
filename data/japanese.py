import requests
import re
import sys
from bs4 import BeautifulSoup
import pandas as pd

columns = [
    "language",
    "infinitive",
    "subject",
    "answer",
    "kana",
    "romaji",
    "en_mood",
    "en_tense",
]

df = pd.DataFrame([], columns=columns)

pattern = re.compile(r"\((.*)\)")

verbs = pd.read_csv("japanese.csv")

url = "https://www.japandict.com/{}"

verb_list = verbs["Verbs"]

verb_length_list = len(verb_list)
counter = 1

language = "japanese"

exceptions = []

for verb in verb_list:
    print(counter, "of", verb_length_list)
    counter += 1

    page = requests.get(url.format(verb))

    soup = BeautifulSoup(page.text, "lxml")

    div = soup.find("div", {"id": "section2"})

    try:
        rows = div.find_all("div", {"class": "row"})
    except:
        exceptions.append(verb)
        continue

    translation_row = rows[0]

    translation_tag = translation_row.find("h2", text="Translation").parent.find_next_sibling("ul")
    translation_lis = translation_tag.find_all("li")

    translations = []

    for li in translation_lis:
        if "list-inline-item" in li.get("class"):
            continue

        translation_text = li.find_all("div")[1].get_text().strip()
        translations.append(translation_text)

    translation = ", ".join(translations)

    section = soup.find("div", {"id": "section2"})

    tables = section.find_all("table")

    if len(tables) == 0:
        exceptions.append(verb)
        continue

    for table in tables:

        thead = table.find("thead")

        sort = thead.get_text().lower()

        tbody = table.find("tbody")

        for tr in tbody.find_all("tr"):

            tense = tr.find("th").get_text().lower()
            answer = tr.find("td").get_text()

            answers = answer.split(" - ")

            answer = answers[0].strip()

            romaji = answers[1].strip()

            english = pattern.search(romaji).group(1)
            i = romaji.index("(")

            kana = romaji[:i]
            kana = kana.strip()

            row = [
                language,
                verb,
                "私",
                answer,
                kana,
                english,
                sort,
                tense,
            ]

            entry = dict(zip(columns, row))

            df = df.append(entry, ignore_index=True)


print(exceptions)
df.to_csv("japanese-final.csv")
