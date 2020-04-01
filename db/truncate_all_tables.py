print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__, __name__, str(__package__)))
from db.database import DB


db = DB()

# Delete all data from the database
db.truncate_all_tables()
db.close()
