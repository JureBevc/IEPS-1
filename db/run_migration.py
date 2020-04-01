from db.database import DB

db = DB()

db.migrate("02_create_field_html_content_hash.sql")
db.migrate("03_insert_page_type_errors.sql")

db.close()
