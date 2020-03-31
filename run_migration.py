from db.db import DB

if __name__ == "__main__":
    db = DB()

    db.migrate("add_disallowed_urls.sql")
    db.migrate("create_field_html_content_hash.sql")
