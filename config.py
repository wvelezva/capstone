import ssl
from datetime import datetime

DATABASE = "content.sqlite"
CREATE_QUESTION_TABLE_SQL = '''
    CREATE TABLE IF NOT EXISTS Question (
        id INTEGER UNIQUE, 
        creation_date INTEGER, 
        question_json BLOB)'''
INSERT_QUESTION = "INSERT OR IGNORE INTO Question (id, creation_date, question_json) VALUES (?, ?, ?)"
MAX_DATE_SQL = "SELECT max(creation_date) FROM Question"

CREATE_PROCESSED_QUESTION_TABLE_SQL = '''
    CREATE TABLE IF NOT EXISTS Processed_Question (
        id INTEGER PRIMARY KEY, 
        creation_date INTEGER, 
        views INTEGER,
        comments INTEGER,
        answers INTEGER,
        answered INTEGER,
        score INTEGER,
        title TEXT,
        body TEXt
        )'''
INSERT_PROCESSED_QUESTION = '''
    INSERT OR IGNORE INTO Processed_Question (id, creation_date, views, comments,answers, answered, score, title, body)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
CREATE_TAG_TABLE_SQL = '''
    CREATE TABLE IF NOT EXISTS Tag (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        question_id INTEGER, 
        tag TEXT,
        FOREIGN KEY(question_id) REFERENCES Processed_Question(id))'''
INSERT_TAG = "INSERT OR IGNORE INTO Tag (question_id, tag) VALUES (?, ?)"

MAX_PROCESSED_QUESTION_ID_SQL = "SELECT max(id) FROM Processed_Question"
QUESTIONS_SQL = "SELECT question_json FROM Question WHERE id > ? ORDER BY id ASC LIMIT 100"

BASE_URL = "https://api.stackexchange.com/2.2/"
API_METHOD = "questions"
PAGESIZE = 100
ORDER = "asc"
SORT = "creation"
SITE = "es.stackoverflow"
FILTER = "!)EhwLgOnQsq.QHlCi6rtwLAT3qaAUe4gZAB*PlSHeKmd3gN)D"

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# print(datetime.fromtimestamp(milliseconds/1000.0))
dt = datetime(2020, 1, 1)
start_date = int(round(dt.timestamp()))
#SLEEP_SECS = 24 * 60 * 60 / 300 #24 hour * 60 ming * 60 seconds / 300 api calls allowed
#SLEEP_SECS = (18 - 9) * 60 * 60 / 300 # only from 9am to 6pm
SLEEP_SECS=10