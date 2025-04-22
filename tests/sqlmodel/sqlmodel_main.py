from models import *
from sqlmodel import Session, select, col, func
from sqlalchemy.orm.exc import NoResultFound
import json
import re
import string

from secrets import secrets

## SQLite
# sqlite_file_name = "yakuaru.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"
# engine = create_engine(sqlite_url)

## PostgreSQL
url = "postgresql+psycopg://{}:{}@{}:{}/test_db".format(secrets['USER'], secrets['PASS'], secrets['IP_ADDRESS'], secrets['PORT'])
engine = create_engine(url)
# engine = create_engine(url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def search(search_term, offset=0, limit=10):
    with Session(engine) as session:
        # Search LIKE
        statement = select(Terms).where(col(Terms.name).contains(search_term)).offset(offset).limit(limit)
        results = session.exec(statement)
        all_results = results.all()
        # print(len(all_results))

        if len(all_results) == 0:
            print("None")
        else:
            for terms in all_results:
                #print(terms)
                print(len(terms.tl))
                for tls in terms.tl:
                    print(tls.definition)
            # for terms in all_results:
            #     print(terms.name)
            #     for tls in terms.tl:
            #         print(tls.definition)
            #         print(tls.src)
            #         try:
            #             print(tls.src[0])
            #         except TypeError:
            #             pass

def search_main(search_term, offset=0, limit=10):
    matches = {}
    with Session(engine) as session:
        # Search LIKE
        statement = select(Terms).where(col(Terms.name).contains(search_term)).offset(offset).limit(limit)
        results = session.exec(statement)
        all_results = results.all()
        # print(len(all_results))

        if len(all_results) == 0:
            print("None")
        else:
            print(all_results)
            for terms in all_results:
                print(terms.name)
            # for terms in all_results:
            #     print(terms.name)
            #     for tls in terms.tl:
            #         print(tls.definition)
            #         print(tls.src)
            #         try:
            #             print(tls.src[0])
            #         except TypeError:
            #             pass

def search_one(search_term):
    with Session(engine) as session:
        statement = select(Terms).where(Terms.name == search_term)
        try:
            one_result = session.exec(statement).one()
            print(one_result is None)
            print(one_result)
            print(one_result.name)
        except NoResultFound:
            print("No result")

def search_TL(search_term):
    with Session(engine) as session:
        statement = select(TL).where(col(TL.definition).contains(search_term))
        try:
            one_result = session.exec(statement).one()
            print(one_result is None)
            print(one_result)
            # print(one_result.name)
        except NoResultFound:
            print("No result")
        
        # for terms in one_result:
        #     print(terms)

def get_term_count():
    with Session(engine) as session:
        statement = select(Terms)
        rows = session.exec(statement)
        return(len(rows.all()))

def get_def_count():
    defs = 0
    with Session(engine) as session:
        statement = select(Terms)
        result = session.exec(statement).all()
        for terms in result:
            defs += len(terms.tl)
        return defs

def term_search(data, search_term:str, letters=False):
    found_list = []
    matches = []
    found = False

    pattern = re.compile(search_term, flags=re.IGNORECASE)

    if not letters:
        for term,value in data.items():

            if pattern.search(term):
                # print(value['altsearch'], "\n")
                found_list.append(value)
                found = True
                # print("FOUND")
            
            if not found:
                if pattern.search(value['altsearch']):
                    # print("ALTFOUND")
                    found_list.append(value)
                    found = True

        if found:
            for item in found_list:
                if pattern.fullmatch(item['term']):
                    # print("MATCH")
                    matches.append(item)
                elif pattern.match(item['term']):
                    # print("SECONDARY MATCH")
                    # print(item)
                    matches.append(item)

            found_list.sort(key=len)
            for item in found_list:
                if item not in matches:
                    # print("NOT FOUND")
                    matches.append(item)
        else:
            return None
    else:
        for term,value in data.items():

            if pattern.match(value['romakana']):
                # print("MATCH")
                # print(term)
                matches.append(value)
    
        matches.sort(key=lambda k: k['term'])

    return matches

create_db_and_tables()
# print("Search One")
# search_one("たしか")
# search_one("仕方")

print("Search all")
print(get_term_count())
print(get_def_count())
search_main("仕方がない")
search_main("大サビ")

search_term = "大サビ"
with open("glossaryMaster.json", "r", encoding="utf8") as file:
    data = json.load(file)
    length = int(len(data))
    terms = term_search(data, search_term)
    print(terms)
# search("仕方がない")
# search("あ",10,3)


# print("Search TL")
# search_TL("cannot")