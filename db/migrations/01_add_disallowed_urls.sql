CREATE TABLE IF NOT EXISTS crawldb.disallowed_url (
  id                   serial  NOT NULL,
  site_id              integer  ,
  url             varchar(3000)   UNIQUE  ,
CONSTRAINT pk_disallowed_url_id PRIMARY KEY ( id )
);

CREATE INDEX IF NOT EXISTS  "idx_disallowed_url_site_id" ON crawldb.disallowed_url ( site_id );

ALTER TABLE crawldb.page DROP CONSTRAINT IF EXISTS fk_disallowed_url_site;
ALTER TABLE crawldb.page ADD CONSTRAINT fk_disallowed_url_site FOREIGN KEY ( site_id ) REFERENCES crawldb.site( id ) ON DELETE CASCADE;
