from datetime import datetime

import psycopg2
import db.db_settings as db_settings
from logger import get_logger

logger = get_logger("db")


class DB:
    conn = None
    cur = None

    def __init__(self, dbname=None):
        self.dbname = dbname if dbname else db_settings.DB_NAME
        self.host = db_settings.DB_HOST
        self.user = db_settings.DB_USER
        self.password = db_settings.DB_PASSWORD
        self.connect()

    def create(self):
        logger.info("Import database '{}'".format(self.dbname))
        self.cur.execute(open("db/crawldb.sql", "r").read())
        self.conn.commit()

    def drop_all_tables(self):
        logger.info("Drop all tables in database '{}'".format(self.dbname))
        self.cur.execute("DROP SCHEMA crawldb CASCADE;")
        self.conn.commit()

    def connect(self):
        if not self.conn or self.conn.closed == 1:
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
                logger.info("Database '{}' connection established".format(self.dbname))

            except psycopg2.Error as e:
                if self.conn:
                    self.conn.rollback()

                logger.error(e.args[0])
                return False

        return True

    def close(self):
        if self.conn:
            self.conn.close()

    def execute(self, query, values):
        retries = 0

        while retries < 5:
            try:
                self.cur.execute(query, values)
                return True
            except Exception as e:
                # Try to reestablish db connection
                logger.error(e)
                try:
                    self.cur.close()
                    self.cur = self.conn.cursor()
                except Exception as e:
                    logger.error(e)
                    self.conn.close()
                    self.connect()

                retries += 1

        # Tried to execute query 5 times, without success
        logger.error(f"Failed to execute query {query}, number of retries: {retries}.")
        return False

    def create_site(self, domain=None, robots_content=None, sitemap_content=None):
        logger.info("Create site: {}".format(domain))
        try:
            query = "INSERT INTO site(domain, robots_content, sitemap_content) VALUES(%s, %s, %s) RETURNING id;"
            values = (domain, robots_content, sitemap_content)
            executed = self.execute(query, values)
            if executed:
                self.conn.commit()
                res = self.cur.fetchone()
                if res:
                    logger.info(f"    Site id: {res[0]}")
                    return res[0]
        except Exception as e:
            logger.error(e)
            self.conn.rollback()
        return None

    def get_site(self, domain=None):
        try:
            query = "SELECT id, robots_content FROM site WHERE domain = %s;"
            executed = self.execute(query, (domain,))
            if executed:
                res = self.cur.fetchone()
                if res:
                    return res[0], res[1]
        except Exception as e:
            logger.error(e)
            self.conn.rollback()

        return None, None

    def get_page(self, url=None):
        try:
            query = "SELECT id FROM page WHERE url = %s;"
            executed = self.execute(query, (url,))
            if executed:
                res = self.cur.fetchone()
                if res:
                    return res[0]
        except Exception as e:
            logger.error(e)
            self.conn.rollback()

        return None

    def create_page(self, site_id=None, page_type_code=None, url=None, html_content=None, http_status_code=None, accessed_time=None):
        if not accessed_time:
            accessed_time = datetime.now()

        # TODO check for duplicates here
        logger.info("Create page: {}".format(url))
        try:
            query = """
                INSERT INTO page(site_id, page_type_code, url, html_content, http_status_code, accessed_time) 
                VALUES(%s, %s, %s, %s, %s, %s) RETURNING id;
            """
            values = (site_id, page_type_code, url, html_content, http_status_code, accessed_time)
            executed = self.execute(query, values)
            if executed:
                self.conn.commit()
                res = self.cur.fetchone()
                if res:
                    logger.info(f"    Page id: {res[0]}")
                    return res[0]
        except Exception as e:
            logger.error(e)
            self.conn.rollback()
        return None

    def set_page_type(self, page_id=None, t=None):
        # HTML
        # BINARY
        # DUPLICATE
        # FRONTIER
        try:
            query = "UPDATE page SET page_type_code = %s WHERE id = %s;"
            self.cur.execute(query, (t, page_id))
            self.conn.commit()
            return self.cur.rowcount
        except Exception as e:
            logger.error(e)
            self.conn.rollback()
        return None

    def create_link(self, from_page=None, to_page=None):
        logger.info("Insert link from {} to {}".format(from_page, to_page))
        try:
            query = "INSERT INTO link(from_page, to_page) VALUES(%s, %s);"
            self.cur.execute(query, (from_page, to_page))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(e)
            self.conn.rollback()
        return None

    def get_types(self):
        self.cur.execute("SELECT * FROM data_type")
        while True:
            row = self.cur.fetchone()
            if row is None:
                break

            logger.info("Data type: " + str(row[0]))
