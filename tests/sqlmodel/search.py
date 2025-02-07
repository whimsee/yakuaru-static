from models import *
from sqlmodel import Session, select, col
from sqlalchemy.orm.exc import NoResultFound

from secrets import secrets

url = "postgresql://{}:{}@{}:{}/yakudb".format(secrets['USER'], secrets['PASS'], secrets['IP_ADDRESS'], secrets['PORT'])
engine = create_engine(url)

async def term_search(data, search_term:str, letters=False):
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