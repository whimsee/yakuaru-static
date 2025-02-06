from models import *
from sqlmodel import Session, select, col

sqlite_file_name = "yakuaru.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

with Session(engine) as session:
    # statement = select(Terms)
    search_term = "仕方"
    # Search LIKE
    statement = select(Terms).where(col(Terms.name).contains(search_term))
    results = session.exec(statement)
    for terms in results:
        # print(terms.tl)
        for tls in terms.tl:
            print(tls.definition)

# import sqlite3

# con = sqlite3.connect("yakuaru.db")
# cur = con.cursor()

# term = "仕方がない"
# search_term = "%" + term + "%"

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

# res = cur.execute("SELECT term, romakana, lit, tl, hepburn, kunrei, nihon, furigana, altsearch FROM terms WHERE term LIKE ?", [search_term])
# get = res.fetchall()
# for hit in get:
#     term, romakana, lit , tl, hepburn, kunrei, nihon, furigana, altsearch = hit
#     print("Term:", term)
#     print("Romakana:", romakana)
#     print("Lit:", lit)
#     print("TL index:", tl)
#     print("Hepburn:", hepburn)
#     print("Kunrei:", kunrei)
#     print("Nihon:", nihon)
#     print("Furigana:", furigana)
#     print("Altsearch:", altsearch)

#     if tl != None:
#         tl_split = tl.split(",")
#         for key in tl_split:
#             print(key)
#             res = cur.execute("SELECT def, defexp, src, samples, credit, image_format, image_caption FROM tl WHERE id = ?", [key])
#             definition, defexp, src, samples, credit, image_format, image_caption = res.fetchone()
#             print("definition:", definition)
#             print("defexp:", defexp)
#             print("src:", src)
#             print("samples:", samples)
#             print("credit:", credit)
#             print("img_format:", image_format)
#             print("img_caption:", image_caption)