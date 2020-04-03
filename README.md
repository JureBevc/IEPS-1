# IEPS-1
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-360/)

Repository for IEPS assignment 1

Running time: 10 hours
Database dump URL: https://easyupload.io/q9uez0

## How to run?
1) Create db_settings.py file in the db directory. You can copy db_settings.example.py and modify it with your data.
2) Create a virtual environment and install requirements (follow Virtual Environment process bellow).
3) Create a database (import from the prepared crawldb.sql script in the db directory) with:
```python -m db.create_database``` and then run migrations with ```python -m db.run_migration```.
4) Run scrape script with ```python scrape.py```, you can pass number of crawlers/threads you want to run as the first argument otherwise 1 crawler will start.

### Virtual environment
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

If the database is running locally, the line \
```self.conn = psycopg2.connect(host="localhost", user="databaseuser", dbname="mydb",                                          password="SecretPassword")``` \
in db.py's ```connect()``` method should be used.
