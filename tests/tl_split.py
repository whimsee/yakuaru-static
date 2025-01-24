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
        
        # print(tl)
        for entries in tl:
            print(entries)
            # for x in entries:
            #     print(get_item(tl, entries, "def"))
            definition = get_tl(entries, "def")
            source = get_tl(entries, "src")
            jpsam = get_tl(entries, "jpsam")
            ensam = get_tl(entries, "ensam")
            credit = get_tl(entries, "credit")
            img = get_tl(entries, "img")

            print(definition)
            print(source)
            print(jpsam)
            print(ensam)
            print(credit)
            print(img)


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