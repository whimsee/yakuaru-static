import sqlite3
import json
import re

def get_item(data, items, field):
    try:
        return data[items][field]
    except KeyError as e:
        return None

con = sqlite3.connect("tutorial.db")
cur = con.cursor()
try:
    cur.execute("""
    CREATE TABLE entry(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    term TEXT NOT NULL, romakana TEXT NOT NULL,
    lit TEXT,
    hepburn TEXT NOT NULL,
    kunrei TEXT NOT NULL,
    nihon TEXT NOT NULL,
    furigana TEXT,
    altsearch TEXT NOT NULL)
    """)
except sqlite3.OperationalError:
    print("Table already exists")


with open('glossaryMaster.json') as file:
    data = json.load(file)

for items in data:
    term = get_item(data, items, "term")
    romakana = get_item(data, items, "romakana")
    lit = get_item(data, items, "lit")
    hepburn = get_item(data, items, "hepburn")
    kunrei = get_item(data, items, "kunrei")
    nihon = get_item(data, items, "nihon")
    furigana = get_item(data, items, "furigana")
    altsearch = get_item(data, items, "altsearch")

    # try:
    cur.execute("""
        INSERT INTO entry("term", "romakana", "lit", "hepburn", "kunrei", "nihon", "furigana", "altsearch") VALUES
        (?,?,?,?,?,?,?,?)
        """, (term, romakana, lit, hepburn, kunrei, nihon, furigana, altsearch))
    con.commit()
    # except Exception as e:
    #     print(e)

res = cur.execute("SELECT * FROM entry")
print(res.fetchall())