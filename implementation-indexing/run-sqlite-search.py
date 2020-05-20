import sys
from db.database import DB
import os
from bs4 import BeautifulSoup
import nltk

nltk.download('stopwords')
nltk.download('punkt')
from data.stopwords import stop_words_slovene
import re

sites = [
    'e-prostor.gov.si',
    'e-uprava.gov.si',
    'evem.gov.si',
    'podatki.gov.si',
]


def get_document_text(doc_name):
    path = None
    for site in sites:
        if doc_name.startswith(site):
            path = site

    file_path = f"data/{path}/{doc_name}"
    print("Reading file " + file_path)
    # Get page text
    soup = BeautifulSoup(open(file_path, 'rb').read(), "html.parser")

    # Remove scripts
    for s in soup.select('script'):
        s.extract()

    return soup.body.get_text()


def sql_search(text):
    print("Results for a query: " + text)

    # Tokenize the query
    tokenized = nltk.word_tokenize(text, language="slovene")

    tokens = [word.lower() for word in tokenized if word not in stop_words_slovene]

    postings = db.get_all_postings(tokens)
    if postings:
        ids = [int(n) for n in postings[0][2].split(",")]
        ids.sort()
        doc_text = get_document_text(postings[0][0])

        max_print = 5
        max_i = 0
        for word_idx in ids:
            print(f"---{postings[0][0]} Index :{word_idx} ---\n")
            print(doc_text[word_idx-5:word_idx+5], end="\n")
            max_i += 1
            if max_i >= max_print:
                break
        print()


if __name__ == "__main__":
    db = DB()
    sql_search(" ".join(sys.argv[1:]))
    db.close()
