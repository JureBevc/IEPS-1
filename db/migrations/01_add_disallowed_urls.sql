CREATE TABLE IF NOT EXISTS crawldb.disallowed_url (
  id                   serial  NOT NULL,
  site_id              integer  NOT NULL,
  url             varchar(3000) NOT NULL,
CONSTRAINT pk_disallowed_url_id PRIMARY KEY ( id )
);

ALTER TABLE crawldb.disallowed_url ADD UNIQUE (site_id, url);
ALTER TABLE crawldb.disallowed_url DROP CONSTRAINT IF EXISTS fk_disallowed_url_site;
ALTER TABLE crawldb.disallowed_url ADD CONSTRAINT fk_disallowed_url_site FOREIGN KEY ( site_id ) REFERENCES crawldb.site( id ) ON DELETE CASCADE;

CREATE INDEX IF NOT EXISTS  "idx_disallowed_url_site_id" ON crawldb.disallowed_url ( site_id );
