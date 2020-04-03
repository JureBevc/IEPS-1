from db.database import DB

db = DB()
starting_pages = [
    "https://www.gov.si/",
    "https://evem.gov.si/evem/drzavljani/zacetna.evem/",
    "https://e-uprava.gov.si/",
    "https://e-prostor.gov.si/"
]
q = "SELECT l.from_page, COUNT(l.to_page) \
 FROM crawldb.link as l \
 GROUP BY l.from_page \
 ORDER BY l.from_page"

executed = db.execute(query=q, values=None)
if executed:
    db.conn.commit()
    res = db.cur.fetchall()
    if res:
        avg = 0
        for r in res:
            avg += r[1]
        avg = avg / len(res)
        print(f"Average number of links per page: {avg}")

q = "SELECT i.page_id, COUNT(i.id) \
 FROM crawldb.image as i \
 GROUP BY i.page_id \
 ORDER BY i.page_id"

executed = db.execute(query=q, values=None)
if executed:
    db.conn.commit()
    res = db.cur.fetchall()
    if res:
        avg = 0
        for r in res:
            avg += r[1]
        avg = avg / len(res)
        print(f"Average number of images per page: {avg}")

q = "SELECT COUNT(i.id) \
 FROM crawldb.image as i"

executed = db.execute(query=q, values=None)
if executed:
    db.conn.commit()
    res = db.cur.fetchall()
    if res:
        print(f"Total number of images: {res[0][0]}")

all_pages = 0

q = "SELECT COUNT(id) \
 FROM crawldb.page as i"

executed = db.execute(query=q, values=None)
if executed:
    db.conn.commit()
    res = db.cur.fetchall()
    if res:
        all_pages = res[0][0]
        print(f"Total number of pages: {all_pages}")

q = "SELECT COUNT(id) \
 FROM crawldb.page as i \
 WHERE i.page_type_code = 'HTML'"

executed = db.execute(query=q, values=None)
if executed:
    db.conn.commit()
    res = db.cur.fetchall()
    if res:
        print(f"Total number of pages of type HTML: {res[0][0]} ({res[0][0] * 100 / all_pages:.2f}%)")

q = "SELECT COUNT(id) \
 FROM crawldb.page as i \
 WHERE i.page_type_code = 'DUPLICATE'"

executed = db.execute(query=q, values=None)
if executed:
    db.conn.commit()
    res = db.cur.fetchall()
    if res:
        print(f"Total number of pages of type DUPLICATE: {res[0][0]} ({res[0][0] * 100 / all_pages:.2f}%)")

q = "SELECT COUNT(id) \
 FROM crawldb.page as i \
 WHERE i.page_type_code = 'FRONTIER'"

executed = db.execute(query=q, values=None)
if executed:
    db.conn.commit()
    res = db.cur.fetchall()
    if res:
        print(f"Total number of pages of type FRONTIER: {res[0][0]} ({res[0][0] * 100 / all_pages:.2f}%)")

q = "SELECT url, COUNT(l.to_page) \
FROM crawldb.link as l \
INNER JOIN crawldb.page ON (l.from_page = crawldb.page.id) \
GROUP BY url \
ORDER BY COUNT(l.to_page) DESC"

executed = db.execute(query=q, values=None)
if executed:
    db.conn.commit()
    res = db.cur.fetchall()
    if res:
        print("Top 5 pages that contain most links to other pages: ")
        for r in range(5):
            print(f"  {r + 1}: {res[r][0]} - {res[r][1]}")

q = "SELECT url, COUNT(l.from_page) \
FROM crawldb.link as l \
INNER JOIN crawldb.page ON (l.to_page = crawldb.page.id) \
GROUP BY url \
ORDER BY COUNT(l.from_page) DESC"

executed = db.execute(query=q, values=None)
if executed:
    db.conn.commit()
    res = db.cur.fetchall()
    if res:
        print("Top 5 pages that contain most links from other pages: ")
        for r in range(5):
            print(f"  {r + 1}: {res[r][0]} - {res[r][1]}")

print("\nStarting page statistics:\n")
for page in starting_pages:
    q = "SELECT url, COUNT(l.to_page) \
     FROM crawldb.link as l \
     INNER JOIN crawldb.page ON (l.from_page = crawldb.page.id) \
     WHERE url='" + page + "' \
     GROUP BY url"

    executed = db.execute(query=q, values=None)
    if executed:
        db.conn.commit()
        res = db.cur.fetchall()
        if res:
            print(f"{page} links to {res[0][1]} pages.")


for page in starting_pages:
    q = "SELECT url, COUNT(i.id) \
     FROM crawldb.image as i \
     INNER JOIN crawldb.page ON (i.page_id = crawldb.page.id) \
     WHERE url='" + page + "' \
     GROUP BY url"

    executed = db.execute(query=q, values=None)
    if executed:
        db.conn.commit()
        res = db.cur.fetchall()
        if res:
            print(f"{page} has {res[0][1]} images.")


for page in starting_pages:
    q = "SELECT url, COUNT(l.from_page) \
     FROM crawldb.link as l \
     INNER JOIN crawldb.page ON (l.to_page = crawldb.page.id) \
     WHERE url='" + page + "' \
     GROUP BY url"

    executed = db.execute(query=q, values=None)
    if executed:
        db.conn.commit()
        res = db.cur.fetchall()
        if res:
            print(f"{page} is linked to by {res[0][1]} pages.")
db.close()
