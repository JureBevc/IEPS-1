import sys
import os
from bs4 import BeautifulSoup
import nltk
import time

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
    # print("Reading file " + file_path)
    # Get page text
    soup = BeautifulSoup(open(file_path, 'r', newline='\n').read(), "html.parser")

    # Remove scripts
    for s in soup.select('script'):
        s.extract()

    return soup.body.get_text()


def generate_postings(tokens):
    postings = []
    for site in sites:
        # Open all HTML files in current site directory
        path = f"data/{site}"
        files = os.listdir(path)

        for doc_name in files:
            if not doc_name.endswith('.html'):
                continue
            frequency = 0
            indexes = ""

            # Get page text
            text = get_document_text(doc_name).lower()

            for word in tokens:
                positions = [str(m.start()) for m in re.finditer(re.escape(word), text)]
                indexes += ",".join(positions) + ","
                frequency += len(positions)
            indexes = indexes[:-2]
            if indexes == "":
                continue
            postings.append((doc_name, frequency, indexes))
    postings.sort(key=lambda tup: tup[1], reverse=True)
    return postings


def basic_search(text):
    print("Results for a query: " + text)

    # Tokenize the query
    tokenized = nltk.word_tokenize(text, language="slovene")

    tokens = [word.lower() for word in tokenized if word not in stop_words_slovene]

    start = time.time()
    postings = generate_postings(tokens)
    elapsed = int((time.time() - start) * 1000)
    print(f"Results found in {elapsed}ms")

    fmt = "{:<14} {:<25} {:<50}"
    print(fmt.format("Frequencies", "Document", "Snippet"))
    print(fmt.format("----------", "-----------------------",
                     "-----------------"))

    max_postings = 5
    postings_i = 0
    for posting in postings:
        ids = [int(n) for n in posting[2].split(",") if n]

        ids.sort()
        doc_text = get_document_text(posting[0])

        snippet = ""
        max_print = 5
        max_i = 0
        character_range = 20
        indexes_in_snippet = []
        for word_idx in ids:
            usable = True
            for used in indexes_in_snippet:
                if abs(word_idx - used) < character_range:
                    usable = False
                    break
            if usable:
                indexes_in_snippet.append(word_idx)
                snippet += doc_text[word_idx - character_range:word_idx + character_range].replace("\n", "") + "..."
                max_i += 1
                if max_i >= max_print:
                    break

        print(fmt.format(posting[1], posting[0], snippet))
        postings_i += 1
        if postings_i >= max_postings:
            break


if __name__ == "__main__":
    basic_search(" ".join(sys.argv[1:]))
