from models import *
from sqlmodel import Session, select, col
from sqlalchemy.orm.exc import NoResultFound

sqlite_file_name = "yakuaru.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

### echo for debug
# engine = create_engine(sqlite_url, echo=True)
engine = create_engine(sqlite_url)

def search(search_term, offset=0, limit=10):
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

def search_one(search_term):
    with Session(engine) as session:
        statement = select(Terms).where(Terms.name == search_term)
        try:
            one_result = session.exec(statement).one()
            print(one_result is None)
            print(one_result.name)
        except NoResultFound:
            print("No result")
        
        # for terms in one_result:
        #     print(terms)

print("Search One")
search_one("たしか")
search_one("仕方")

print("Search all")
search("あ",10,3)