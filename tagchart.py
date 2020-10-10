import sqlite3
import time
from config import *

conn = sqlite3.connect(DATABASE)
cur = conn.cursor()

cur.execute('select tag, count(*) from tag group by tag order by count(*) desc limit 10')
tags = list()
for tag_row in cur:
    tags.append(tag_row[0])

print("Top 10 tags")
print(tags)

cur.execute('''
    SELECT tag, strftime('%Y%m',date(pq.creation_date,'unixepoch')), count(*) 
    from Processed_Question pq, tag t
    where pq.id=t.question_id
    group by 1, 2
    ''')

months = list()
monthly_tags = dict()
for tag_row in cur:
    month = tag_row[1]
    if month not in months:
        months.append(month)

    tag = tag_row[0]
    count = tag_row[2]
    monthly_tags[(month, tag)] = count

months.sort()

fhand = open('tagchart.js','w')
fhand.write("tagchart = [ ['Month'")
for tag in tags:
    fhand.write(",'"+tag+"'")
fhand.write("]")

for month in months[:-1]:
    fhand.write(",\n['"+month+"'")
    for tag in tags:
        key = (month, tag)
        val = monthly_tags.get(key, 0)
        fhand.write(","+str(val))
    fhand.write("]");

fhand.write("\n];\n")
fhand.close()

print("Output written to tagchart.js")
print("Open tagchart.htm to visualize the data")
