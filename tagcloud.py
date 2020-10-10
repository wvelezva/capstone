import sqlite3
from config import *

conn = sqlite3.connect(DATABASE)
cur = conn.cursor()

cur.execute('select tag, count(*) from tag group by tag order by count(*) desc limit 100')
counts = dict()
for tag_row in cur:
    counts[tag_row[0]] = tag_row[1]

highest = None
lowest = None
for k in counts:
    if highest is None or highest < counts[k]:
        highest = counts[k]
    if lowest is None or lowest > counts[k]:
        lowest = counts[k]
print('Range of counts:', highest, lowest)

# Spread the font sizes across 20-100 based on the count
bigsize = 80
smallsize = 20

fhand = open('tagcloud.js', 'w')
fhand.write("tags = [")
first = True
for k in counts:
    if not first:
        fhand.write(",\n")
    first = False
    size = counts[k]
    size = (size - lowest) / float(highest - lowest)
    size = int((size * bigsize) + smallsize)
    fhand.write("{text: '" + k + "', size: " + str(size) + "}")
fhand.write("\n];\n")
fhand.close()

print("Output written to tagcloud.js")
print("Open tagcloud.htm in a browser to see the visualization")
