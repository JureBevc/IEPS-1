from db.database import DB
import os
from bs4 import BeautifulSoup


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

for site in sites:
    # Open all HTML files in current site directory
    path = f"data/{site}"
    files = os.listdir(path)

    for file in files:
        if not file.endswith('.html'):
            continue

        soup = BeautifulSoup(open(f"{path}/{file}", 'rb').read())
        print(soup.get_text())
