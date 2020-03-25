import sqlite3 as lite


class DB:
    conn = None
    cur = None

    def __init__(self, dbname):
        self.dbname = dbname
        self.connect()

    def create(self):

        drop_datatype = "DROP TABLE IF EXISTS data_type"

        create_datatype = """
            CREATE TABLE data_type ( 
            code     varchar(20)  NOT NULL,
            CONSTRAINT   pk_data_type_code PRIMARY KEY (code)
            );
        """

        drop_pagetype = "DROP TABLE IF EXISTS page_type"

        create_pagetype = """CREATE TABLE page_type ( 
            code    varchar(20)  NOT NULL,	
            CONSTRAINT  pk_page_type_code PRIMARY KEY ( code )
            );
        """

        drop_site = "DROP TABLE IF EXISTS site"

        create_site = """CREATE TABLE site ( 
        id                   serial  NOT NULL,
        "domain"             varchar(500)  ,
        robots_content       text  ,
        sitemap_content      text  ,
        CONSTRAINT pk_site_id PRIMARY KEY ( id )
        );
    """

        drop_page = "DROP TABLE IF EXISTS page"

        create_page = """CREATE TABLE page ( 
        id                   serial  NOT NULL,
        site_id              integer  ,
        page_type_code       varchar(20)  ,
        url                  varchar(3000)  ,
        html_content         text  ,
        http_status_code     integer  ,
        accessed_time        timestamp  ,
        CONSTRAINT pk_page_id PRIMARY KEY ( id ),
        CONSTRAINT unq_url_idx UNIQUE ( url ) 
        ); 
    """
        drop_idx_page_site_id = "DROP INDEX IF EXISTS idx_page_site_id"

        create_idx_page_site_id = "CREATE INDEX idx_page_site_id ON page ( site_id )"

        create_idx_page_page_type_code = "CREATE INDEX idx_page_page_type_code ON page ( page_type_code );"

        drop_idx_page_page_type_code = "DROP INDEX IF EXISTS idx_page_page_type_code"

        drop_page_data = "DROP TABLE IF EXISTS page_data"

        create_page_data = """CREATE TABLE page_data ( 
        id                   serial  NOT NULL,
        page_id              integer  ,
        data_type_code       varchar(20)  ,
        "data"               bytea,
        CONSTRAINT pk_page_data_id PRIMARY KEY ( id )
        );
    """

        drop_idx_page_data_page_id = "DROP INDEX IF EXISTS idx_page_data_page_id"

        create_idx_page_data_page_id = "CREATE INDEX idx_page_data_page_id ON page_data ( page_id )"

        drop_idx_page_data_data_type_code = "DROP INDEX IF EXISTS idx_page_data_data_type_code"

        create_idx_page_data_data_type_code = "CREATE INDEX idx_page_data_data_type_code ON" \
                                              " page_data ( data_type_code );"

        drop_image = "DROP TABLE IF EXISTS image"

        create_image = """CREATE TABLE image ( 
            id                   serial  NOT NULL,
            page_id              integer  ,
            filename             varchar(255)  ,
            content_type         varchar(50)  ,
            "data"               bytea  ,
            accessed_time        timestamp  ,
            CONSTRAINT pk_image_id PRIMARY KEY ( id )
            );     
        """

        drop_idx_image_page_id = "DROP INDEX IF EXISTS idx_image_page_id"

        create_idx_image_page_id = "CREATE INDEX idx_image_page_id ON image ( page_id )"

        drop_link = "DROP TABLE IF EXISTS link"

        create_link = """CREATE TABLE link ( 
            from_page            integer  NOT NULL,
            to_page              integer  NOT NULL,
            CONSTRAINT _0 PRIMARY KEY ( from_page, to_page )
            )
        """

        drop_idx_link_from_page = "DROP INDEX IF EXISTS idx_link_from_page"

        create_idx_link_from_page = "CREATE INDEX idx_link_from_page ON link ( from_page )"

        drop_idx_link_to_page = "DROP INDEX IF EXISTS idx_link_to_page"

        create_idx_link_to_page = "CREATE INDEX idx_link_to_page ON link ( to_page )"

        fk_image = "ALTER TABLE image ADD CONSTRAINT  fk_image_page_data FOREIGN KEY ( page_id )" \
                   " REFERENCES page( id ) ON DELETE RESTRICT"

        fk_link_page = "ALTER TABLE link ADD CONSTRAINT fk_link_page FOREIGN KEY ( from_page )" \
                       " REFERENCES page( id ) ON DELETE RESTRICT"

        fk_link_page_1 = "ALTER TABLE link ADD CONSTRAINT fk_link_page_1 FOREIGN KEY ( to_page )" \
                         " REFERENCES page( id ) ON DELETE RESTRICT"

        fk_page_site = "ALTER TABLE page ADD CONSTRAINT fk_page_site FOREIGN KEY ( site_id )" \
                       " REFERENCES site( id ) ON DELETE RESTRICT"

        fk_page_page_type = "ALTER TABLE page ADD CONSTRAINT fk_page_page_type FOREIGN KEY ( page_type_code )" \
                            " REFERENCES page_type( code ) ON DELETE RESTRICT"

        fk_page_data_page = "ALTER TABLE page_data ADD CONSTRAINT fk_page_data_page FOREIGN KEY ( page_id )" \
                            " REFERENCES page( id ) ON DELETE RESTRICT"

        fk_page_data_data_type = "ALTER TABLE page_data ADD CONSTRAINT fk_page_data_data_type FOREIGN KEY " \
                                 "( data_type_code ) REFERENCES data_type( code ) ON DELETE RESTRICT"

        insert_data_type_vals = """INSERT INTO data_type VALUES 
            ('PDF'),
            ('DOC'),
            ('DOCX'),
            ('PPT'),
            ('PPTX')
            
        """

        insert_page_type_vals = """INSERT INTO page_type VALUES 
            ('HTML'),
            ('BINARY'),
            ('DUPLICATE'),
            ('FRONTIER')
        """


        self.cur.execute(drop_datatype)
        self.cur.execute(create_datatype)
        self.cur.execute(drop_pagetype)
        self.cur.execute(create_pagetype)
        self.cur.execute(drop_site)
        self.cur.execute(create_site)
        self.cur.execute(drop_page)
        self.cur.execute(create_page)
        self.cur.execute(create_idx_page_site_id)
        self.cur.execute(drop_idx_page_site_id)
        self.cur.execute(create_idx_page_page_type_code)
        self.cur.execute(drop_idx_page_page_type_code)
        self.cur.execute(drop_page_data)
        self.cur.execute(create_page_data)
        self.cur.execute(drop_idx_page_data_page_id)
        self.cur.execute(create_idx_page_data_page_id)
        self.cur.execute(drop_idx_page_data_data_type_code)
        self.cur.execute(create_idx_page_data_data_type_code)
        self.cur.execute(drop_image)
        self.cur.execute(create_image)
        self.cur.execute(drop_idx_image_page_id)
        self.cur.execute(create_idx_image_page_id)
        self.cur.execute(drop_link)
        self.cur.execute(create_link)
        self.cur.execute(drop_idx_link_from_page)
        self.cur.execute(create_idx_link_from_page)
        self.cur.execute(drop_idx_link_to_page)
        self.cur.execute(create_idx_link_to_page)

        # sqlite does not allow adding constraints to existing tables
        """
        self.cur.execute(fk_image)
        self.cur.execute(fk_link_page)
        self.cur.execute(fk_link_page_1)
        self.cur.execute(fk_page_site)
        self.cur.execute(fk_page_page_type)
        self.cur.execute(fk_page_data_page)
        self.cur.execute(fk_page_data_data_type)
        """

        self.cur.execute(insert_data_type_vals)
        self.cur.execute(insert_page_type_vals)

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


