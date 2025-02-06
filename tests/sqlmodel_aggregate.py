from sqlmodel import Field, Session, Relationship, SQLModel, select, create_engine, col

class termTL_link(SQLModel, table=True):
    term_id: int | None = Field(default=None, foreign_key="terms.id", primary_key=True)
    tl_id: int | None = Field(default=None, foreign_key="tl.id", primary_key=True)

class tlSample_link(SQLModel, table=True):
    tl_id: int | None = Field(default=None, foreign_key="tl.id", primary_key=True)
    sample_id: int | None = Field(default=None, foreign_key="samples.id", primary_key=True)

class TL(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    definition: str
    defexp: str | None = None
    src: str | None = None
    credit: str | None = None
    image_format: str | None = None
    image_caption: str | None = None

    samples: list["Samples"] = Relationship(back_populates="tls", link_model=tlSample_link)

class Samples(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    jpsam: str
    ensam: str | None = None

class Terms(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    romakana: str
    lit: str | None = None
    hepburn: str | None = None
    kunrei: str | None = None
    nihon: str | None = None
    furigana: str | None = None
    altsearch: str | None = None

    tl: list["TL"] = Relationship(back_populates="terms", link_model=termTL_link)


sqlite_file_name = "yakutest.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)

# import sqlite3
# import json
# import re

# class TermExistsError(Exception):
#     pass

# def get_item(data, items, field):
#     try:
#         return data[items][field]
#     except KeyError as e:
#         return None

# def get_tl(data, field):
#     try:
#         return data[field]
#     except KeyError as e:
#         return None

# def insert_samples(jpsam, ensam):
#     try:
#         cur.execute("""
#             INSERT INTO "samples" ("jpsam", "ensam") VALUES
#             (?,?)
#             """, (jpsam, ensam))
#         con.commit()
#         ID = str(cur.lastrowid)
#         print(ID)
#         return ID
#     except Exception as e:
#         print(e)

# with sqlite3.connect("yakuaru.db") as con:
#     with open('glossaryMaster.json') as file:
#         data = json.load(file)

#         # Init cursor
#         cur = con.cursor()

#         # Create tables
#         print("Creating terms table")
#         try:
#             cur.execute("""
#                 CREATE TABLE IF NOT EXISTS "terms" (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 term TEXT UNIQUE NOT NULL,
#                 romakana TEXT NOT NULL,
#                 lit TEXT,
#                 tl TEXT,
#                 hepburn TEXT NOT NULL,
#                 kunrei TEXT NOT NULL,
#                 nihon TEXT NOT NULL,
#                 furigana TEXT,
#                 altsearch TEXT NOT NULL
#             )
#             """)
#         except sqlite3.OperationalError:
#             print("Table already exists")

#         print("Creating tl table")
#         try:
#             cur.execute("""
#                 CREATE TABLE IF NOT EXISTS "tl" (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 def TEXT NOT NULL,
#                 defexp TEXT,
#                 src TEXT,
#                 samples TEXT,
#                 credit TEXT,
#                 image_format TEXT,
#                 image_caption TEXT
#             )
#             """)
#         except sqlite3.OperationalError:
#             print("Table already exists")

#         print("Creating samples table")
#         try:
#             cur.execute("""
#                 CREATE TABLE IF NOT EXISTS "samples" (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 jpsam TEXT NOT NULL,
#                 ensam TEXT NOT NULL
#             )
#             """)
#         except sqlite3.OperationalError:
#             print("Table already exists")

#         ### Each Term = item
#         for items in data:
#             term = get_item(data, items, "term")
#             romakana = get_item(data, items, "romakana")
#             lit = get_item(data, items, "lit")
#             hepburn = get_item(data, items, "hepburn")
#             kunrei = get_item(data, items, "kunrei")
#             nihon = get_item(data, items, "nihon")
#             furigana = get_item(data, items, "furigana")
#             altsearch = get_item(data, items, "altsearch")

#             tl = get_item(data, items, "tl")

#             res = cur.execute("SELECT term FROM terms WHERE term = ?", [term])
#             if res.fetchone() == None:
#                 try:
#                     cur.execute("""
#                         INSERT INTO "terms" ("term", "romakana", "lit", "hepburn", "kunrei", "nihon", "furigana", "altsearch") VALUES
#                         (?,?,?,?,?,?,?,?)
#                         """, (term, romakana, lit, hepburn, kunrei, nihon, furigana, altsearch))
#                     con.commit()
#                     TERM_ID = cur.lastrowid
#                     print(TERM_ID)
#                 except Exception as e:
#                     print(e)
#                     break
#             else:
#                 print(term, "already exists. Skipping.")
#                 continue
#                 # raise TermExistsError("Term must be updated instead")
            
#             # print(tl)

#             ### Each Definition = defs in Term
#             TL_ID = []
#             for defs in tl:
#                 # print(defs)
#                 definition = get_tl(defs, "def")
#                 defexp = get_tl(defs, "defexp")
#                 source_temp = get_tl(defs, "src")
#                 jpsam = get_tl(defs, "jpsam")
#                 ensam = get_tl(defs, "ensam")
#                 credit_temp = get_tl(defs, "credit")

#                 # prep source. convert list to string with separator
#                 if source_temp != None:
#                     if isinstance(source_temp, list):
#                         source = "^".join(str(x) for x in source_temp)
#                     else:
#                         source = source_temp
#                 else:
#                     source = None

#                 # prep credit. convert list to string with separator
#                 if credit_temp != None:
#                     if isinstance(credit_temp, list):
#                         credit = "^".join(str(x) for x in credit_temp)
#                     else:
#                         credit = credit_temp
#                 else:
#                     credit = None

#                 ## each img
#                 # check if img exists and set parameters
#                 img = get_tl(defs, "img")
#                 if img != None:
#                     img_format = img[0]
#                     img_caption = img[1]
#                     # try:
#                     #     img_caption = img[1]
#                     # except IndexError:
#                     #     img_caption = None
#                 else:
#                     img_format = None
#                     img_caption = None
                
#                 ## each sample
#                 # check if samples exist for samples table
#                 if jpsam != None and ensam != None:
#                     sample_entries = {
#                         "jpsam" : jpsam,
#                         "ensam" : ensam
#                         }
#                     samples = insert_samples(jpsam, ensam)
#                 else:
#                     samples = None


#                 print(definition)
#                 print(defexp)
#                 print(source)
#                 print(jpsam)
#                 print(ensam)
#                 print(samples)
#                 print(credit)
#                 print(img)

#                 cur.execute("""
#                     INSERT INTO "tl" ("def", "defexp", "src", "samples", "credit", "image_format", "image_caption") VALUES
#                     (?,?,?,?,?,?,?)
#                     """, (definition, defexp, source, samples, credit, img_format, img_caption))
#                 con.commit()
#                 TL_ID.append(cur.lastrowid)
#             print(TL_ID)
#             TL = ",".join(str(x) for x in TL_ID)
#             print(TL)
#             cur.execute("""
#                 UPDATE "terms" SET tl=? WHERE id = ?
#                         """, (TL, TERM_ID))
#             con.commit()
#             # break
            

# #  def
# #     defexp
# #     src[]
# #     samples
# #         - id
# #         - jpsam
# #         - ensam
# #     jpsam (refer to samples)
# #     ensam (refer to samples)
# #     credit
# #     genre[](remove)
# #     image 
# #         - id
# #         - link