import sqlite3
import urllib.parse
import urllib.request
from io import BytesIO
import gzip
import time
import json
from config import *


def maxquestiondate(cur):
    # Pick up where we left off
    cur.execute(MAX_DATE_SQL)
    row = cur.fetchone()
    if row is not None:
        if row[0] is None:
            return start_date
        else:
            return row[0]

    return None


conn = sqlite3.connect(DATABASE)
cur = conn.cursor()
cur.execute(CREATE_QUESTION_TABLE_SQL)
conn.commit()

parms = dict()
parms["pagesize"] = PAGESIZE
parms["order"] = ORDER
parms["sort"] = SORT
parms["site"] = SITE
parms["filter"] = FILTER
parms["fromdate"] = maxquestiondate(cur)
parms["page"] = 1
while True:

    url = BASE_URL + API_METHOD + "?" + urllib.parse.urlencode(parms)
    print("Page", parms["page"])
    print(url)

    text = "None"
    try:
        # Open with a timeout of 30 seconds
        document = urllib.request.urlopen(url, None, 30, context=ctx)
        if document.getcode() != 200:
            print("Error code=", document.getcode(), url)
            break

        if document.info().get('Content-Encoding') == 'gzip':
            buf = BytesIO(document.read())
            f = gzip.GzipFile(fileobj=buf)
            text = f.read().decode()
        else:
            text = document.read.decode()

        print("Uncompressed Response size", len(text))

    except KeyboardInterrupt:
        print('')
        print('Program interrupted by user...')
        break
    except Exception as e:
        print("Unable to retrieve or parse page", url)
        print("Error", e)
        break

    try:
        js = json.loads(text)
    except:
        print(text)  # We print in case unicode causes an error
        break

    print("JSON Response Elements")
    for k in js:
        if k != "items" and k != "quota_max":
            print(k, js[k])

    if "error_id" in js:
        print("Error in json response", js["error_id"])
        break

    for item in js["items"]:
        try:
            id = item["question_id"]
            creation = item["creation_date"]
            cur.execute(INSERT_QUESTION, (id, creation, json.dumps(item)))
        except Exception as e:
            print("Unable to save the item ", item)
            print("Error", e)

    conn.commit()

    if not js["has_more"] or "quota_remaining" not in js or js["quota_remaining"] == 0:
        break;

    backoff = 0
    if "backoff" in js and "quota_remaining" in js and js["quota_remaining"] > 0:
        backoff = js["backoff"] + 2
        parms["page"] = parms["page"] + 1
    elif "quota_remaining" not in js or js["quota_remaining"] == 0:
        backoff = 1 * 60 * 60  # 1 hour
        parms["page"] = 1
        parms["fromdate"] = creation
    else:
        parms["page"] = parms["page"] + 1

    secs = max(SLEEP_SECS, backoff)
    print('Pausing for', secs, 'secs')
    time.sleep(secs)

cur.close()
print("Scrapping stackoverflow ends")
