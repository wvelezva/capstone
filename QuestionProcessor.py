import sqlite3
import json
from config import *


def lastprocessedquestion():
    # Pick up where we left off
    cur.execute(MAX_PROCESSED_QUESTION_ID_SQL)
    row = cur.fetchone()
    return 1 if row[0] is None else row[0]


conn = sqlite3.connect(DATABASE)
cur = conn.cursor()
cur.execute(CREATE_PROCESSED_QUESTION_TABLE_SQL)
cur.execute(CREATE_TAG_TABLE_SQL)
conn.commit()

while True:

    lastProcessedQuestion = lastprocessedquestion()
    print("last processed question - ", lastProcessedQuestion)

    cur.execute(QUESTIONS_SQL, (lastProcessedQuestion, ))
    rows = cur.fetchall()
    if len(rows) == 0:
        break;

    for row in rows:
        try:
            js = json.loads(row[0])
        except:
            print(row[0])  # We print in case unicode causes an error
            continue

        try:
            id = js["question_id"]
            creation_date = js["creation_date"]
            views = js["view_count"]
            comments = js["comment_count"]
            answers = js["answer_count"]
            answered = js["is_answered"]
            score = js["score"]
            title = js["title"]
            body = js["body"]
            tags = js["tags"]
        except Exception as e:
            print(e)
            continue

        print(id)
        print(tags)
        # print(title)
        # print(body)

        cur.execute(INSERT_PROCESSED_QUESTION, (id, creation_date, views, comments, answers, answered, score, title, body))

        for tag in tags:
            cur.execute(INSERT_TAG, (id, tag))

    conn.commit()

cur.close()
print("Question processing ends")