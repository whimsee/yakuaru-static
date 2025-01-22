import sqlite3
import json
con = sqlite3.connect("tutorial.db")
cur = con.cursor()
# # cur.execute("CREATE TABLE movie(title, year, score)")

index = [2,6,8,1,7,3]

res = cur.execute("SELECT key FROM keys")

keys_raw = res.fetchone()[0]
print(keys_raw)
keys_strip = keys_raw.strip("[]")
keys_split = keys_strip.split(",")

for num in keys_split:
    print(index[int(num)])
    item = int(index[int(num)])
    print("SELECT {} FROM {} WHERE id = {}".format("value", "val", item))
    res = cur.execute("SELECT {} FROM {} WHERE id = {}".format("value", "vals", item))
    print(cur.fetchall())

con.close()

# with open('glossaryMaster.json') as file:
#     data = json.load(file)

# for items in data:
#     # print(data[items])
#     print(data[items]["tl"])