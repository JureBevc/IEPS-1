from db.database import DB


db = DB()

# Delete all data from the database
db.truncate_all_tables()
db.close()
