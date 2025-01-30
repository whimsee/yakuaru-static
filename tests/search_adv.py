import sqlite3

con = sqlite3.connect("yakuaru.db")
cur = con.cursor()

term = "仕方がない"
search_term = "%" + term + "%"

# res = cur.execute("SELECT * FROM terms WHERE term = ?", [term])
# get = res.fetchone()
# print(get)
# if get:
#     print("Yes")
# else:
#     print("None")

# res = cur.execute("SELECT tl FROM terms WHERE term = ?", [term])
# if res != None:
#     print(res.fetchone())
# else:
#     print("No tl")

# res = cur.execute("SELECT * FROM terms")
# get = res.fetchall()
# for x in get:
#     print(x)

res = cur.execute("SELECT * FROM terms WHERE term LIKE ?", [search_term])
get = res.fetchall()
for hit in get:
    print(hit)