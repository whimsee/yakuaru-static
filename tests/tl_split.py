import sqlite3
import json
import re

def get_item(data, items, field):
    try:
        return data[items][field]
    except KeyError as e:
        return None

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
        tl = get_item(data, items, "tl")
        
        print(tl)
        for entries in tl:
            print(entries)
        
        break