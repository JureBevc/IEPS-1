import psycopg2

from db import db_settings
from logger import get_logger


class DB:

    def __init__(self, dbname=None, logger=None):
        if not logger:
            logger = get_logger("db")

        self.logger = logger
        self.dbname = dbname if dbname else db_settings.DB_NAME
        self.host = db_settings.DB_HOST
        self.user = db_settings.DB_USER
        self.password = db_settings.DB_PASSWORD

        self.conn = None
        self.cur = None
        self.connect()

    def create(self):
        self.logger.info("Import database '{}' from db/migrations/crawldb.sql".format(self.dbname))
        self.cur.execute(open("db/migrations/crawldb.sql", "r").read())
        self.conn.commit()

    def drop_all_tables(self):
        self.logger.info("Drop all tables in database '{}'".format(self.dbname))
        self.cur.execute("DROP SCHEMA crawldb CASCADE;")
        self.conn.commit()

    def truncate_all_tables(self):
        self.logger.info("Truncate all tables in database '{}'".format(self.dbname))
        tables = ['page_data', 'image', 'link', 'page', 'site']
        for table in tables:
            self.cur.execute(f"TRUNCATE {table} CASCADE;")
        self.conn.commit()

    def migrate(self, file):
        self.logger.info("Migrate database '{}' with file: {}".format(self.dbname, file))
        self.cur.execute(open(f"db/migrations/{file}", "r").read())
        self.conn.commit()

    def connect(self):

        if not self.conn or self.conn.closed == 1:

            # Create threaded connection pool
            number_of_connections = 1
            # DSN = f"postgresql://{self.user}:{self.password}@{self.host}/{self.dbname}"
            # tcp = ThreadedConnectionPool(1, number_of_connections, DSN)

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
                self.logger.info("Database '{}' connection established".format(self.dbname))

            except psycopg2.Error as e:
                if self.conn:
                    self.conn.rollback()

                self.logger.error(e.args[0])
                return False

        return True

    def close(self):
        self.logger.info("Close connection")
        if self.cur:
            self.cur.close()

        if self.conn:
            self.conn.close()

    def execute(self, query, values):
        retries = 0

        # If transaction can be executed they can be commited, else it must be rollback
        while retries < 5:
            try:
                self.cur.execute(query, values)
                return True
            except Exception as e:
                # Try to reestablish db connection
                self.logger.error(e)
                try:
                    self.cur.close()
                    self.cur = self.conn.cursor()
                except Exception as e:
                    self.logger.error(e)
                    self.conn.close()
                    self.connect()

                retries += 1

        # Tried to execute query 5 times, without success
        self.logger.error(f"Failed to execute query {query}, number of retries: {retries}.")
        return False

    def create_site(self, domain=None, robots_content=None, sitemap_content=None):
        self.logger.info("Create site with domain: {}".format(domain))
        try:
            query = "INSERT INTO site(domain, robots_content, sitemap_content) VALUES(%s, %s, %s) RETURNING id;"
            values = (domain, robots_content, sitemap_content)
            executed = self.execute(query, values)
            if executed:
                self.conn.commit()
                res = self.cur.fetchone()
                if res:
                    self.logger.info(f"    New site was created, id: {res[0]}")
                    return res[0]
        except Exception as e:
            self.logger.error(e)
            self.conn.rollback()
        return None

    def create_image(self, page_id, filename, content_type, accessed_time):
        self.logger.info(
            f"Create image with filename {filename}, content type {content_type} and accessed time {accessed_time}")
        try:
            query = "INSERT INTO image(page_id, filename, content_type, accessed_time) VALUES(%s, %s, %s, %s) RETURNING id;"
            values = (page_id, filename, content_type, accessed_time)
            executed = self.execute(query, values)
            if executed:
                self.conn.commit()
                res = self.cur.fetchone()
                if res:
                    self.logger.info(f"    New image was created, id: {res[0]}")
                    return res[0]
        except Exception as e:
            self.logger.error(e)
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
            self.logger.error(e)
            self.conn.rollback()

        return None, None

    def get_all_sites(self, has_robots=False):
        where_robots = ""
        if has_robots:
            where_robots = " WHERE robots_content IS NOT NULL"
        query = f"SELECT id, robots_content FROM site{where_robots};"
        try:
            executed = self.execute(query, ())
            if executed:
                return self.cur.fetchall()
        except Exception as e:
            self.logger.error(e)
            self.conn.rollback()

        return []

    def get_page(self, url=None):
        try:
            query = "SELECT id, page_type_code FROM page WHERE url = %s;"
            executed = self.execute(query, (url,))
            if executed:
                res = self.cur.fetchone()
                if res:
                    return res[0], res[1]
        except Exception as e:
            self.logger.error(e)
            self.conn.rollback()

        return None, None

    def get_page_by_url_and_type(self, url=None, page_type=None):
        try:
            query = "SELECT id FROM page WHERE url = %s AND data_type = %s;"
            executed = self.execute(query, (url, page_type))
            if executed:
                res = self.cur.fetchone()
                if res:
                    return res[0]
        except Exception as e:
            self.logger.error(e)
            self.conn.rollback()

        return None

    def get_page_by_hash(self, html_content_hash=None):
        try:
            query = "SELECT id, site_id FROM page WHERE html_content_hash = %s;"
            executed = self.execute(query, (html_content_hash,))
            if executed:
                res = self.cur.fetchone()
                if res:
                    return res[0], res[1]
        except Exception as e:
            self.logger.error(e)
            self.conn.rollback()

        return None, None

    def get_pages_by_type(self, page_type_code=None):
        try:
            query = "SELECT url FROM page WHERE page_type_code = %s;"
            executed = self.execute(query, (page_type_code,))
            if executed:
                urls = self.cur.fetchall()
                return urls
        except Exception as e:
            self.logger.error(e)
            self.conn.rollback()

        return None, None

    def create_page(self, site_id=None, page_type_code=None, url=None, html_content=None, http_status_code=None,
                    accessed_time=None, html_content_hash=None):
        self.logger.info(f"Create a new {page_type_code} page with url: {url}")

        if page_type_code == "DUPLICATE":
            query = """
                INSERT INTO page(site_id, page_type_code, http_status_code, accessed_time, html_content_hash) 
                VALUES(%s, %s, %s, %s, %s) RETURNING id;
            """
            values = (site_id, page_type_code, http_status_code, accessed_time, html_content_hash)
        else:
            query = """
                INSERT INTO page(site_id, page_type_code, url, html_content, http_status_code, accessed_time, html_content_hash) 
                VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id;
            """
            values = (site_id, page_type_code, url, html_content, http_status_code, accessed_time, html_content_hash)

        try:
            executed = self.execute(query, values)
            if executed:
                self.conn.commit()
                res = self.cur.fetchone()
                if res:
                    self.logger.info(f"    New {page_type_code} page was created, id: {res[0]}.")
                    return res[0]
        except Exception as e:
            self.logger.error(e)
            self.conn.rollback()
        return None

    def update_page(self, page_id=None, fields=None):
        if not page_id or not fields:
            return None

        try:
            fields_string = ""
            for key in fields.keys():
                fields_string += f" {key} = %s,"

            query = f"UPDATE page SET{fields_string[:-1]} WHERE id = %s;"
            values = tuple(list(fields.values()) + [page_id])
            self.cur.execute(query, values)
            self.conn.commit()
            return self.cur.rowcount
        except Exception as e:
            self.logger.error(e)
            self.conn.rollback()
        return None

    def set_page_type(self, page_id=None, page_type_code=None):
        # HTML
        # BINARY
        # DUPLICATE
        # FRONTIER
        try:
            query = "UPDATE page SET page_type_code = %s WHERE id = %s;"
            self.cur.execute(query, (page_type_code, page_id))
            self.conn.commit()
            return self.cur.rowcount
        except Exception as e:
            self.logger.error(e)
            self.conn.rollback()
        return None

    def create_link(self, from_page=None, to_page=None):
        self.logger.info("Create a link from page {} to page {}".format(from_page, to_page))
        try:
            query = "INSERT INTO link(from_page, to_page) VALUES(%s, %s);"
            self.cur.execute(query, (from_page, to_page))
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(e)
            self.conn.rollback()
        return None

    def create_page_data(self, page_id=None, data_type_code=None, data=None):
        self.logger.info(f"Create page {page_id} data with type: {data_type_code}")
        try:
            query = "INSERT INTO page_data(page_id, data_type_code, data) VALUES(%s, %s, %s);"
            self.cur.execute(query, (page_id, data_type_code, data))
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(e)
            self.conn.rollback()
        return None

    def get_types(self):
        self.cur.execute("SELECT * FROM data_type")
        while True:
            row = self.cur.fetchone()
            if row is None:
                break

            self.logger.info("Data type: " + str(row[0]))
