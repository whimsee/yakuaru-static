from models import *
from sqlmodel import Session, select, col
from sqlalchemy.orm.exc import NoResultFound

from secrets import secrets

## SQLite
# sqlite_file_name = "yakuaru.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"
# engine = create_engine(sqlite_url)

## PostgreSQL
url = "postgresql://{}:{}@{}:{}/yakudb".format(secrets['USER'], secrets['PASS'], secrets['IP_ADDRESS'], secrets['PORT'])
engine = create_engine(url)
# engine = create_engine(url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def search(search_term, offset=0, limit=10):
    create_db_and_tables()
    with Session(engine) as session:
        # Search LIKE
        statement = select(Terms).where(col(Terms.name).contains(search_term)).offset(offset).limit(limit)
        results = session.exec(statement)
        all_results = results.all()
        print(len(all_results))

        if len(all_results) == 0:
            print("None")
        else:
            for terms in all_results:
                print(terms.name)
                for tls in terms.tl:
                    print(tls.definition)
                    print(tls.src)
                    try:
                        print(tls.src[0])
                    except TypeError:
                        pass

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

print("Search One")
search_one("たしか")
search_one("仕方")

print("Search all")
search("仕方がない")
search("あ",10,3)


print("Search TL")
search_TL("cannot")