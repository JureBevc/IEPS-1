from db.database import DB
import os
from bs4 import BeautifulSoup
import nltk
from data.stopwords import stop_words_slovene
import re


"""
     Prior to indexing we need to retrieve textual data from web pages. To get whole textual data, you can 
     call appropriate text() function from your favourite HTML parsing library. The text must be then 
     preprocesed  using tokenization (see word_tokenize function within the nltk.tokenize package), stopword 
     removal (use these stopwords or extend them) and normalization into lowercase letters. If you apply 
     additional preprocessing steps, document them in the report. Note that the same preprocessing function 
     needs to be applied to a given query by a user.
"""

sites = [
    'e-prostor.gov.si',
    'e-uprava.gov.si',
    'evem.gov.si',
    'podatki.gov.si',
]

nltk.download('stopwords')
nltk.download('punkt')


db = DB()
# db.create()

for site in sites:
    # Open all HTML files in current site directory
    path = f"data/{site}"
    files = os.listdir(path)
    print(f"\n\n{site}")

    for doc_name in files:
        if not doc_name.endswith('.html'):
            continue
        print(doc_name)

        # Get page text
        soup = BeautifulSoup(open(f"{path}/{doc_name}", 'rb').read(), "html.parser")

        # Remove scripts
        for s in soup.select('script'):
            s.extract()

        text = soup.body.get_text()

        # Tokenize page text
        # tokenized = StringTokenizer.tokenize(text)
        tokenized = nltk.word_tokenize(text, language="slovene")

        for word in tokenized:
            # Remove stopwords & lowercase letter normalization
            token = word.lower()
            if token not in stop_words_slovene:
                # Insert tokenized word into IndexWord if it doesn't exist yet
                db.create_index_word(token)

                # Get word appearance indexes in the original document
                indexes = [str(m.start()) for m in re.finditer(re.escape(word), text)]
                frequency = len(indexes)

                # Check if posting exists
                posting = db.get_posting(token, doc_name)

                if not posting:
                    db.create_posting(token, doc_name, frequency, ",".join(indexes))
                else:
                    # Combine indexes with new found indexes to prevent duplicates
                    unique_indexes = set(posting[3].split(',') + indexes)

                    # Check if indices have changed: there are new indexes, update database
                    if len(unique_indexes) != posting[2]:
                        db.update_posting(token, doc_name, len(unique_indexes), ",".join(unique_indexes))

db.close()
