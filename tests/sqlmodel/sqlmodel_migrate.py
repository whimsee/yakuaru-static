from models import *
from sqlmodel import Session, select, col

import json
import re

from secrets import secrets

POSTGRES = False

### SQLite
# sqlite_file_name = "yakuaru.db"
# url = f"sqlite:///{sqlite_file_name}"
# engine = create_engine(url, echo=True)

## Mariadb
# url = "mysql+pymysql://{}:{}@{}:{}/yakudb?charset=utf8mb4".format(secrets['USER'], secrets['PASS'], secrets['IP_ADDRESS'], secrets['PORT'])
# engine = create_engine(url, echo=True)

## PostgreSQL
url = "postgresql://{}:{}@{}:{}/test_db".format(secrets['USER'], secrets['PASS'], secrets['IP_ADDRESS'], secrets['PORT'])
# engine = create_engine(url, echo=True)
engine = create_engine(url)
POSTGRES = True


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

class TermExistsError(Exception):
    pass

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

if __name__ == "__main__":
    create_db_and_tables()
    with open('glossaryMaster.json') as file:
        data = json.load(file)

        ### Each Term = item
        for items in data:
            term = get_item(data, items, "term")
            altterm = get_item(data, items, "altterm")
            romakana = get_item(data, items, "romakana")
            lit = get_item(data, items, "lit")
            hepburn = get_item(data, items, "hepburn")
            kunrei = get_item(data, items, "kunrei")
            nihon = get_item(data, items, "nihon")
            furigana = get_item(data, items, "furigana")
            # altsearch = get_item(data, items, "altsearch")

            tl = get_item(data, items, "tl")

            # Add term check later
            
            ### Each Definition = defs in Term
            TL_TERMS = []
            for defs in tl:
                # print(defs)
                definition = get_tl(defs, "def")
                defexp = get_tl(defs, "defexp")
                source_temp = get_tl(defs, "src")
                jpsam = get_tl(defs, "jpsam")
                ensam = get_tl(defs, "ensam")
                credit_temp = get_tl(defs, "credit")
            
                ### Prep source. convert list to string with separator
                if source_temp != None:
                    if POSTGRES:
                        source = source_temp
                    elif POSTGRES == False and isinstance(source_temp, list):
                        source = "^*".join(str(x) for x in source_temp)
                    else:
                        source = source_temp
                else:
                    source = None

                ### Prep credit. convert list to string with separator
                if credit_temp != None:
                    if POSTGRES:
                        credit = credit_temp
                    elif POSTGRES == False and isinstance(credit_temp, list):
                        credit = "^*".join(str(x) for x in credit_temp)
                    else:
                        credit = credit_temp
                else:
                    credit = None


                ### each img
                # check if img exists and set parameters
                img = get_tl(defs, "img")
                if img != None:
                    img_format = img[0]
                    img_caption = img[1]
                    # try:
                    #     img_caption = img[1]
                    # except IndexError:
                    #     img_caption = None
                else:
                    img_format = None
                    img_caption = None

                tl_add = TL(
                    definition=definition,
                    defexp=defexp,
                    src=source,
                    credit=credit,
                    jpsam=jpsam,
                    ensam=ensam,
                    image_format=img_format,
                    image_caption=img_caption,
                )

                TL_TERMS.append(tl_add)

            term_add = Terms(
                name=term,
                altterm=altterm,
                romakana=romakana,
                lit=lit,
                hepburn=hepburn,
                kunrei=kunrei,
                nihon=nihon,
                furigana=furigana,
                # altsearch=altsearch,
                tl=TL_TERMS
            )

            with Session(engine) as session:
                print("Adding:", term)
                session.add(term_add)
                session.commit()
