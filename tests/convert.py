import sqlite3
import json
# con = sqlite3.connect("tutorial.db")
# cur = con.cursor()
# # cur.execute("CREATE TABLE movie(title, year, score)")

# res = cur.execute("SELECT name FROM sqlite_master")
# print(res.fetchone())
# con.close()

with open('glossaryMaster.json') as file:
    data = json.load(file)

for items in data:
    # print(data[items])
    print(data[items]["tl"])