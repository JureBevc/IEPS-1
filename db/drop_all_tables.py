from db.database import DB

db = DB()

# Drop all tables from the database
db.drop_all_tables()
db.close()
