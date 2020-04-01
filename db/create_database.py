from db.database import DB

db = DB()

# Create tables from db/migrations/crawldb.sql
db.create()

db.close()
