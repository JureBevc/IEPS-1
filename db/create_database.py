from db.database import DB

if __name__ == "__main__":
    db = DB()

    # Create tables from db/migrations/crawldb.sql
    db.create()

    db.close()
