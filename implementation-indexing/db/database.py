import sqlite3 as lite


class DB:
    """
        The table IndexWord must contain a list of all words that are indexed by your system.
        Related table Posting contains frequencies and offset indexes for a word in a specific
        document. Let’s say that a word davek appears three times at indexes 2, 34 and 894 in
        a document evem.gov.si/evem.gov.si.4.html. A record in a Posting table would look
        like the following: (‘davek’, ‘evem.gov.si/evem.gov.si.4.html’, 3, ‘2,34,894’).
    """
    conn = None
    cur = None

    def __init__(self):
        self.connect()

    def create(self):
        create_index_word = '''
            CREATE TABLE IndexWord (
              word TEXT PRIMARY KEY
            );
        '''

        create_posting = '''
            CREATE TABLE Posting (
              word TEXT NOT NULL,
              documentName TEXT NOT NULL,
              frequency INTEGER NOT NULL,
              indexes TEXT NOT NULL,
              PRIMARY KEY(word, documentName),
              FOREIGN KEY (word) REFERENCES IndexWord(word)
            );
        '''

        self.cur.execute(create_index_word)
        self.cur.execute(create_posting)
        self.conn.commit()

    def connect(self):
        if not self.conn:
            try:
                self.conn = lite.connect("inverted-index.db")
                self.cur = self.conn.cursor()

            except lite.Error as e:
                if self.conn:
                    self.conn.rollback()

                print("Error {}:".format(e.args[0]))

    def close(self):
        if self.conn:
            self.conn.close()

    def create_posting(self, word=None, doc_name=None, frequency=None, indexes=None):
        self.cur.execute("INSERT INTO Posting(word, documentName, frequency, indexes) VALUES (?, ?, ?, ?)", (word, doc_name, frequency, indexes))
        self.conn.commit()

    def create_index_word(self, word=""):
        self.cur.execute("INSERT INTO IndexWord(word) VALUES (?)", word)
        self.conn.commit()
