from db.database import DB

if __name__ == "__main__":
    db = DB()

    # Delete all data from the database
    db.truncate_all_tables()
    db.close()
