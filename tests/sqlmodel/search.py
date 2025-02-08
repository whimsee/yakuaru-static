from models import *
from sqlmodel import Session, select, col
from sqlalchemy.orm.exc import NoResultFound

from secrets import secrets

url = "postgresql://{}:{}@{}:{}/yakudb".format(secrets['USER'], secrets['PASS'], secrets['IP_ADDRESS'], secrets['PORT'])
# connect_args = {"check_same_thread": False}
# engine = create_engine(url, echo=True, connect_args=connect_args)
engine = create_engine(url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def term_search(search_term:str, letters=False, offset=0, limit=0):
    found_list = []
    matches = []
    found = False

    with Session(engine) as session:
        statement = select(Terms).where(col(Terms.name).contains(search_term)).offset(offset).limit(limit)
        result = session.exec(statement)
        hit = result.all()
        print(len(hit))

create_db_and_tables()

term_search("仕方")
#     if not letters:
#         for term,value in data.items():

#             if pattern.search(term):
#                 # print(value['altsearch'], "\n")
#                 found_list.append(value)
#                 found = True
#                 # print("FOUND")
            
#             if not found:
#                 if pattern.search(value['altsearch']):
#                     # print("ALTFOUND")
#                     found_list.append(value)
#                     found = True

#         if found:
#             for item in found_list:
#                 if pattern.fullmatch(item['term']):
#                     # print("MATCH")
#                     matches.append(item)
#                 elif pattern.match(item['term']):
#                     # print("SECONDARY MATCH")
#                     # print(item)
#                     matches.append(item)

#             found_list.sort(key=len)
#             for item in found_list:
#                 if item not in matches:
#                     # print("NOT FOUND")
#                     matches.append(item)
#         else:
#             return None
#     else:
#         for term,value in data.items():

#             if pattern.match(value['romakana']):
#                 # print("MATCH")
#                 # print(term)
#                 matches.append(value)
    
#         matches.sort(key=lambda k: k['term'])

#     return matches