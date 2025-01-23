import sqlite3

con = sqlite3.connect("tutorial.db")
cur = con.cursor()

term = "無理はしないでね"
res = cur.execute("SELECT term FROM entry WHERE term = ?", [term])
print(res.fetchall())