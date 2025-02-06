from models import *
from sqlmodel import Session, select, col
from sqlalchemy.orm.exc import NoResultFound

sqlite_file_name = "yakuaru.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

### echo for debug
# engine = create_engine(sqlite_url, echo=True)
engine = create_engine(sqlite_url)

with Session(engine) as session:
    # statement = select(Terms)
    # search_term = "["
    # search_term = "仕方"
    search_term = "あ"
    # Search LIKE
    statement = select(Terms).where(col(Terms.name).contains(search_term))
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

    search_term = "たしか"
    # search_term = "仕方"

    statement = select(Terms).where(Terms.name == search_term)
    results = session.exec(statement)
    try:
        one_result = results.one()
        print(one_result is None)
        print(one_result.name)
    except NoResultFound:
        print("No result")
    
    # for terms in one_result:
    #     print(terms)