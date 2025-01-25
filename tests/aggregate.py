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

def insert_samples(jpsam, ensam):
    try:
        cur.execute("""
            INSERT INTO "samples" ("jpsam", "ensam") VALUES
            (?,?)
            """, (jpsam, ensam))
        con.commit()
        ID = str(cur.lastrowid)
        print(ID)
        return ID
    except Exception as e:
        print(e)

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
            def TEXT NOT NULL,
            defexp TEXT NOT NULL,
            src TEXT,
            samples TEXT,
            credit TEXT NOT NULL,
            image TEXT NOT NULL
            )
            """)
        except sqlite3.OperationalError:
            print("Table already exists")

        print("Creating samples table")
        try:
            cur.execute("""
            CREATE TABLE "samples" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jpsam TEXT UNIQUE NOT NULL,
            ensam TEXT NOT NULL
            )
            """)
        except sqlite3.OperationalError:
            print("Table already exists")

        ### Each Term = item
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

            ### Each Definition = defs in Term
            for defs in tl:
                # print(defs)
                definition = get_tl(defs, "def")
                defexp = get_tl(defs, "defexp")
                source = get_tl(defs, "src")
                jpsam = get_tl(defs, "jpsam")
                ensam = get_tl(defs, "ensam")
                credit = get_tl(defs, "credit")

                ## each img
                # check if img exists and set parameters
                img = get_tl(defs, "img")
                if img != None:
                    img_format = img[0]
                    img_caption = img[1]
                else:
                    img_format = None
                    img_caption = None
                
                ## each sample
                # check if samples exist for samples table
                if jpsam != None and ensam != None:
                    sample_entries = {
                        "jpsam" : jpsam,
                        "ensam" : ensam
                        }
                    samples = insert_samples(jpsam, ensam)
                else:
                    samples = None


                print(definition)
                print(defexp)
                print(source)
                print(jpsam)
                print(ensam)
                print(samples)
                print(credit)
                print(img)

                cur.execute("""
                        INSERT INTO "tl" ("def", "defexp", "src", "samples", "credit", "img") VALUES
                        (?,?,?,?,?,?)
                        """, (definition, defexp, source, samples, credit, img))
                con.commit()
                TL_ID = cur.lastrowid
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