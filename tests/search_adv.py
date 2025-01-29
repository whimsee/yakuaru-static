import sqlite3

con = sqlite3.connect("yakuaru.db")
cur = con.cursor()

term = "仕方がない"
res = cur.execute("SELECT * FROM terms WHERE term = ?", [term])
get = res.fetchone()
print(get)
if get:
    print("Yes")
else:
    print("None")

res = cur.execute("SELECT tl FROM terms WHERE term = ?", [term])
if res != None:
    print(res.fetchone())
else:
    print("No tl")