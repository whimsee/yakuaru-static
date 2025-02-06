from models import *
from sqlmodel import Session, select, col

sqlite_file_name = "yakuaru.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

### echo for debug
# engine = create_engine(sqlite_url, echo=True)
engine = create_engine(sqlite_url)

with Session(engine) as session:
    # statement = select(Terms)
    search_term = "仕方"
    # Search LIKE
    statement = select(Terms).where(col(Terms.name).contains(search_term))
    results = session.exec(statement)
    for terms in results:
        print(terms.name)
        for tls in terms.tl:
            print(tls.definition)