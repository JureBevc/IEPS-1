import sqlite3 as lite


class DB:
    conn = None
    cur = None

    def __init__(self, dbname):
        self.dbname = dbname
        self.connect()

    def create(self):
        drop_link_table = "DROP TABLE IF EXISTS link"

        create_link_table = '''
            CREATE TABLE link(
                id     INTEGER PRIMARY KEY AUTOINCREMENT, 
                title   TEXT, 
                url   TEXT, 
                parent_link   INTEGER, 
                FOREIGN KEY(parent_link) REFERENCES link(id)
            );
        '''

        self.cur.execute(drop_link_table)
        self.cur.execute(create_link_table)

        self.conn.commit()

    def connect(self):
        if not self.conn:
            try:
                self.conn = lite.connect(self.dbname)
                self.cur = self.conn.cursor()

            except lite.Error as e:
                if self.conn:
                    self.conn.rollback()

                print("Error {}:".format(e.args[0]))

    def close(self):
        if self.conn:
            self.conn.close()

    def insert(self, title="", url=None, parent_link=None):
        print("Insert row: {}".format(url))
        self.cur.execute("INSERT INTO link(title, url, parent_link) VALUES (?, ?, ?)", (title, url, parent_link))
        self.conn.commit()


