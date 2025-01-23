import json

def get_item(data, items, field):
    try:
        return data[items][field]
    except KeyError as e:
        return None

with open('glossaryMaster.json') as file:
    data = json.load(file)

for items in data:
    # print(data[items])
    # print(data[items]["tl"])
    term = get_item(data, items, "term")
    romakana = get_item(data, items, "romakana")
    lit = get_item(data, items, "lit")
    hepburn = get_item(data, items, "hepburn")
    kunrei = get_item(data, items, "kunrei")
    nihon = get_item(data, items, "nihon")
    furigana = get_item(data, items, "furigana")
    altsearch = get_item(data, items, "altsearch")
    print(term)
    print(romakana)
    print(lit)
    print(hepburn)
    print(kunrei)
    print(nihon)
    print(furigana)
    print(altsearch)
    print("========")