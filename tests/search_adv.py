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

res = cur.execute("SELECT term,romakana,lit,tl,hepburn,kunrei,nihon,furigana,altsearch FROM terms WHERE term LIKE ?", [search_term])
get = res.fetchall()
for hit in get:
    term,romakana,lit,tl,hepburn,kunrei,nihon,furigana,altsearch = hit
    print("Term:", term)
    print("Romakana:", romakana)
    print("Lit:", lit)
    print("TL index:", tl)
    print("Hepburn:", hepburn)
    print("Kunrei:", kunrei)
    print("Nihon:", nihon)
    print("Furigana:", furigana)
    print("Altsearch:", altsearch)

# term TEXT UNIQUE NOT NULL,
#                 romakana TEXT NOT NULL,
#                 lit TEXT,
#                 tl TEXT,
#                 hepburn TEXT NOT NULL,
#                 kunrei TEXT NOT NULL,
#                 nihon TEXT NOT NULL,
#                 furigana TEXT,
#                 altsearch TEXT NOT NULL