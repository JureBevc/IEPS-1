from database import DB

if __name__ == "__main__":
    db = DB()

    # Drop all tables from the database
    db.drop_all_tables()
    db.close()
