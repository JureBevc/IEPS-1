# IEPS-1
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-360/)

Repository for IEPS assignment 1

### TODO
- [x] Extend the database with a hash or compare exact HTML code @lukatavcer
- [ ] 10 bonus points for locally sensitive hashing
- [ ] Include links from href attributes and onclick JS events
- [ ] Detect images on a web page
- [x] Check if duplicate exist
    - check already parsed urls
    - check urls in frontier
    - check by html content hash
- [x] Fetch and check robots.txt
- [x] Respect 5 sec request rule (not only domain, IP too)
#
#### Virtual environment
https://docs.python-guide.org/dev/virtualenvs/
1) create virtualenv
2) activate virtualenv ```source venv/bin/activate```
3) ```pip install -r requirements.txt```

#
#### Database

The database can run in a docker container with the command \
```docker run --name postgresql-wier -e POSTGRES_PASSWORD=SecretPassword -e POSTGRES_USER=user -v $PWD/init-scripts:/docker-entrypoint-initdb.d  -p 5432:5432 -d postgres:9``` \
If it is running this way, the line \
```self.conn = psycopg2.connect(host="localhost", user="user",  password="SecretPassword")``` \
in db.py's ```connect()``` method should be used.

The database can be run locally in the following way: 
1) install postgreSQL and set the appropriate environment variables 
2) create a database: \
```$psql -d template1 -U postgres``` \
A prompt for ```template1=#``` should appear. Enter the following commands: \
```CREATE USER databaseuser WITH PASSWORD 'SecretPassword';``` \
```CREATE DATABASE mydb;``` \
```GRANT ALL PRIVILEGES ON DATABASE mydb to databaseuser;``` \
 ```\q``` 
 3) You can test the database with \
 ```$psql mydb databaseuser```, \
 where SQL statements can be executed.

Note, that these instructions are written for Windows 10 and may differ on other systems

If the database is running locally, the line \
```self.conn = psycopg2.connect(host="localhost", user="databaseuser", dbname="mydb",                                          password="SecretPassword")``` \
in db.py's ```connect()``` method should be used.

 
