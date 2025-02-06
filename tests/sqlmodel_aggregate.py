from models import *
from sqlmodel import Session, select, col

import json
import re

sqlite_file_name = "yakutest.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

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

if __name__ == "__main__":
    create_db_and_tables()
    with open('glossaryMaster.json') as file:
        data = json.load(file)

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

            # term_add = Terms(
            #     name=term,
            #     romakana=romakana,
            #     lit=lit,
            #     hepburn=hepburn,
            #     kunrei=kunrei,
            #     nihon=nihon,
            #     furigana=furigana,
            #     altsearch=altsearch
            #     tl=TL_TERMS
            # )

            # print(term_add)
            tl = get_item(data, items, "tl")
            print(tl)

            # Add term check later
            
            ### Each Definition = defs in Term
            TL_TERMS = []
            for defs in tl:
                print(defs)
                definition = get_tl(defs, "def")
                defexp = get_tl(defs, "defexp")
                source_temp = get_tl(defs, "src")
                jpsam = get_tl(defs, "jpsam")
                ensam = get_tl(defs, "ensam")
                credit_temp = get_tl(defs, "credit")
            
                ### Prep source. convert list to string with separator
                if source_temp != None:
                    if isinstance(source_temp, list):
                        source = "^".join(str(x) for x in source_temp)
                    else:
                        source = source_temp
                else:
                    source = None

                ### prep credit. convert list to string with separator
                if credit_temp != None:
                    if isinstance(credit_temp, list):
                        credit = "^".join(str(x) for x in credit_temp)
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
                
                ### each sample
                # check if samples exist for samples table
                if jpsam != None and ensam != None:
                    samples = []
                    # temp_sample = Samples(jpsam=jpsam, ensam=ensam)
                    # samples.append(temp_sample)
                else:
                    samples = None

                tl_add = TL(
                    definition=definition,
                    defexp=defexp,
                    src=source,
                    credit=credit,
                    image_format=img_format,
                    image_caption=img_caption,
                    samples=None
                )

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

                # print(definition)
                # print(defexp)
                # print(source)
                # print(jpsam)
                # print(ensam)
                # print(samples)
                # print(credit)
                # print(img)


            break

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


