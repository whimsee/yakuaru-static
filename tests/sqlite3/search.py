import sqlite3

con = sqlite3.connect("tutorial.db")
cur = con.cursor()

term = "仕方がない"
res = cur.execute("SELECT term FROM entries WHERE term = ?", [term])
get = res.fetchone()
print(get)
if get:
    print("Yes")
else:
    print("None")