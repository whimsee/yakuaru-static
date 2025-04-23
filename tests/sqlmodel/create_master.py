import json
import cutlet
import re
import string
import wanakana
import pykakasi

def strip_punc(text):
    return ' '.join(word.strip(string.punctuation) for word in text.split())

def strip_punc_and_space(text):
    return ''.join(word.strip(string.punctuation) for word in text.split())


def generate_furigana(text):
    temp = ""
    result = kks.convert(text)
    for item in result:
        temp += item['hira']
    return temp

hepburn = cutlet.Cutlet(use_foreign_spelling=False)
kunrei = cutlet.Cutlet(system="kunrei",use_foreign_spelling=False)
nihon = cutlet.Cutlet(system="nihon",use_foreign_spelling=False)

kks = pykakasi.kakasi()

with open("glossaryRaw.json", "r", encoding="utf8") as file:
    data = json.load(file)

    mas_terms = {}
    for x in data:
        term = x

        if x['term'] == "":
            print("This term is empty")
            raise EmptyTerm

        term['termStripped'] = [strip_punc_and_space(x['term'])]
        term['hasKatakana'] = wanakana.is_katakana(strip_punc_and_space(x['term'])) 
        term['hepburn'] = hepburn.romaji(x['romakana']).replace(" ","").lower();
        term['kunrei'] = kunrei.romaji(x['romakana']).replace(" ","").lower();
        term['nihon'] = nihon.romaji(x['romakana']).replace(" ","").lower();
        
        if "altterm" in x.keys():
            for y in x['altterm']:
                term['termStripped'].append(y)
        
        term['altsearch'] = ""
        for y in x['tl']:
            term['altsearch'] += strip_punc_and_space(y['def'])

        if "kanaOverride" in x.keys():
            term['furigana'] = x['kanaOverride']
            term['altsearch'] += wanakana.to_hiragana(x['kanaOverride']) + term['hepburn']
        else:
            for z in x['term']:
                if wanakana.is_kanji(z):
                    term['furigana'] = generate_furigana(x['term'])
                    break
            term['altsearch'] += (wanakana.to_hiragana(x['term']) if wanakana.is_katakana(x['term']) else generate_furigana(x['term'])) + term['hepburn'] 

        mas_terms.update({x['term'].lower() : term})

    
    
#     print(mas_terms['vtr'])
#     print(mas_terms['仕方がない'])
#     print(len(mas_terms))
    
with open("glossaryMaster.json", "w", encoding="utf8") as file:
    json.dump(mas_terms, file,  ensure_ascii=False, indent="\t", separators=(',', ' : '))