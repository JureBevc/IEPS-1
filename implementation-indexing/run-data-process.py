from db.database import DB
import os
from bs4 import BeautifulSoup
import nltk
from data.stopwords import stop_words_slovene


# db = DB()
# db.create()
# db.close()

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

print(stop_words_slovene)
for site in sites:
    # Open all HTML files in current site directory
    path = f"data/{site}"
    files = os.listdir(path)

    for file in files:
        if not file.endswith('.html'):
            continue

        # Get page text
        soup = BeautifulSoup(open(f"{path}/{file}", 'rb').read(), "html.parser")
        text = soup.get_text()

        # Tokenize page text
        # tokenized = StringTokenizer.tokenize(text)
        tokenized = nltk.word_tokenize(text, language="slovene")

        cleaned = []

        # Remove stopwords & lowercase letter normalization
        for token in tokenized:
            token = token.lower()
            if token not in stop_words_slovene:
                cleaned.append(token)

                # Index token
