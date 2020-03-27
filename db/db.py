import psycopg2
import db.db_settings as db_settings


class DB:
    conn = None
    cur = None

    def __init__(self, dbname):
        self.dbname = dbname if dbname else db_settings.DB_NAME
        self.host = db_settings.DB_HOST
        self.user = db_settings.DB_USER
        self.password = db_settings.DB_PASSWORD
        self.connect()

    def create(self):
        print("Import database '{}'".format(self.dbname))
        self.cur.execute(open("db/crawldb.sql", "r").read())
        self.conn.commit()

    def connect(self):
        if not self.conn:
            try:
                # Docker:
                # self.conn = psycopg2.connect(host="localhost", user="user",  password="SecretPassword")
                # Local:
                self.conn = psycopg2.connect(
                    database=self.dbname,
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    options="-c search_path=crawldb"
                )
                self.cur = self.conn.cursor()
                print("Database '{}' connection established".format(self.dbname))

            except psycopg2.Error as e:
                if self.conn:
                    self.conn.rollback()

                print("Error {}:".format(e.args[0]))

    def close(self):
        if self.conn:
            self.conn.close()

    def create_site(self, domain=None, robots_content=None, sitemap_content=None):
        print("Insert site: {}".format(domain))
        try:
            query = "INSERT INTO site(domain, robots_content, sitemap_content) VALUES(%s, %s, %s) RETURNING id;"
            self.cur.execute(query, (domain, robots_content, sitemap_content))
            self.conn.commit()
            site_id = self.cur.fetchone()[0]
            print(f"  Site id: {site_id}")
        except Exception as e:
            print(e)
        return None

    def test(self):
        self.cur.execute("SELECT * FROM crawldb.data_type")
        while True:
            row = self.cur.fetchone()
            if row is None:
                break

            print("Data type: " + str(row[0]))
