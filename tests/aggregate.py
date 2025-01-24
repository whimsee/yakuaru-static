import sqlite3
import json
import re

def get_item(data, items, field):
    try:
        return data[items][field]
    except KeyError as e:
        return None

def get_tl(data, field):
    try:
        return data[field]
    except KeyError as e:
        return None

with sqlite3.connect("tutorial.db") as con:
    with open('glossaryMaster.json') as file:
        data = json.load(file)

        # Init cursor
        cur = con.cursor()

        # Create tables
        print("Creating entries table")
        try:
            cur.execute("""
            CREATE TABLE "entries" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            term TEXT UNIQUE NOT NULL,
            romakana TEXT NOT NULL,
            lit TEXT,
            tl TEXT,
            hepburn TEXT NOT NULL,
            kunrei TEXT NOT NULL,
            nihon TEXT NOT NULL,
            furigana TEXT,
            altsearch TEXT NOT NULL
            )
            """)
        except sqlite3.OperationalError:
            print("Table already exists")

        print("Creating tl table")
        try:
            cur.execute("""
            CREATE TABLE "tl" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            def TEXT UNIQUE NOT NULL,
            defexp TEXT NOT NULL,
            src TEXT,
            samples TEXT,
            credit TEXT NOT NULL,
            image TEXT NOT NULL
            )
            """)
        except sqlite3.OperationalError:
            print("Table already exists")

        
        for items in data:
            term = get_item(data, items, "term")
            romakana = get_item(data, items, "romakana")
            lit = get_item(data, items, "lit")
            hepburn = get_item(data, items, "hepburn")
            kunrei = get_item(data, items, "kunrei")
            nihon = get_item(data, items, "nihon")
            furigana = get_item(data, items, "furigana")
            altsearch = get_item(data, items, "altsearch")

            tl = get_item(data, items, "tl")

            res = cur.execute("SELECT term FROM entries WHERE term = ?", [term])
            if res.fetchone() == None:
                try:
                    cur.execute("""
                        INSERT INTO "entries" ("term", "romakana", "lit", "hepburn", "kunrei", "nihon", "furigana", "altsearch") VALUES
                        (?,?,?,?,?,?,?,?)
                        """, (term, romakana, lit, hepburn, kunrei, nihon, furigana, altsearch))
                    con.commit()
                    ENTRY_ID = cur.lastrowid
                    print(ENTRY_ID)
                except Exception as e:
                    print(e)
                    break
            
            # print(tl)
            for defs in tl:
                print(defs)
                definition = get_tl(defs, "def")
                defexp = get_tl(defs, "defexp")
                source = get_tl(defs, "src")
                jpsam = get_tl(defs, "jpsam")
                ensam = get_tl(defs, "ensam")
                credit = get_tl(defs, "credit")
                img = get_tl(defs, "img")
                samples = []

                print(definition)
                print(defexp)
                print(source)
                print(jpsam)
                print(ensam)
                print(credit)
                print(img)

                cur.execute("""
                        INSERT INTO "tl" ("def", "defexp", "src", "samples", "credit", "img") VALUES
                        (?,?,?,?,?,?)
                        """, (term, romakana, lit, hepburn, kunrei, nihon, furigana, altsearch))



            break

#  def
#     defexp
#     src[]
#     samples
#         - id
#         - jpsam
#         - ensam
#     jpsam (refer to samples)
#     ensam (refer to samples)
#     credit
#     genre[](remove)
#     image 
#         - id
#         - link