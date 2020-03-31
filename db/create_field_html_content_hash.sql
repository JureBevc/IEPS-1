ALTER TABLE crawldb.page ADD html_content_hash varchar(3000)   UNIQUE;

CREATE INDEX IF NOT EXISTS  "idx_html_content_hash" ON crawldb.page ( html_content_hash );