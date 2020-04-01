from db.database import DB

if __name__ == "__main__":
    db = DB()

    db.migrate("migrations/01_add_disallowed_urls.sql")
    db.migrate("migrations/02_create_field_html_content_hash.sql")
    db.migrate("migrations/03_insert_page_type_errors.sql")

    db.close()
