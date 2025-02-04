from sqlmodel import Field, Session, SQLModel, select, create_engine, col

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None


class Terms(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    term: str
    romakana: str
    lit: str | None = None
    tl: str | None = None
    hepburn: str
    kunrei: str
    nihon: str
    furigana: str | None = None
    altsearch: str

        #    cur.execute("""
        #         CREATE TABLE IF NOT EXISTS "terms" (
        #         id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         term TEXT UNIQUE NOT NULL,
        #         romakana TEXT NOT NULL,
        #         lit TEXT,
        #         tl TEXT,
        #         hepburn TEXT NOT NULL,
        #         kunrei TEXT NOT NULL,
        #         nihon TEXT NOT NULL,
        #         furigana TEXT,
        #         altsearch TEXT NOT NULL
        #     )
        #     """)
        # except sqlite3.OperationalError:
        #     print("Table already exists")

        # print("Creating tl table")
        # try:
        #     cur.execute("""
        #         CREATE TABLE IF NOT EXISTS "tl" (
        #         id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         def TEXT NOT NULL,
        #         defexp TEXT,
        #         src TEXT,
        #         samples TEXT,
        #         credit TEXT,
        #         image_format TEXT,
        #         image_caption TEXT
        #     )
        #     """)
        # except sqlite3.OperationalError:
        #     print("Table already exists")

        # print("Creating samples table")
        # try:
        #     cur.execute("""
        #         CREATE TABLE IF NOT EXISTS "samples" (
        #         id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         jpsam TEXT NOT NULL,
        #         ensam TEXT NOT NULL
        #     )
        #     """)
        # except sqlite3.OperationalError:
        #     print("Table already exists")

sqlite_file_name = "yakuaru.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)



def select_terms():
    with Session(engine) as session:
        terms_hit = []
        # Two methods: Second is safer without the %
        # statement = select(Terms).where(Terms.term.like("%ない%"))
        statement = select(Terms).where(col(Terms.term).contains("事"))
        results = session.exec(statement)
        for term in results:
            print(term.term)
            print(term.tl)
            # if term.tl != None:
                # tl_statement = select(Terms).where(col(Terms.term).contains("事"))


def main():
    select_terms()


if __name__ == "__main__":
    main()