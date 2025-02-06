from sqlmodel import SQLModel, create_engine, Field, Relationship

class termTL_link(SQLModel, table=True):
    term_id: int | None = Field(default=None, foreign_key="terms.id", primary_key=True)
    tl_id: int | None = Field(default=None, foreign_key="tl.id", primary_key=True)

class TL(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    definition: str
    defexp: str | None = None
    src: str | None = None
    credit: str | None = None
    jpsam: str | None = None
    ensam: str | None = None
    image_format: str | None = None
    image_caption: str | None = None

    terms: list["Terms"] = Relationship(back_populates="tl", link_model=termTL_link)

class Terms(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    romakana: str
    lit: str | None = None
    hepburn: str | None = None
    kunrei: str | None = None
    nihon: str | None = None
    furigana: str | None = None
    altsearch: str | None = None

    tl: None | list["TL"] = Relationship(back_populates="terms", link_model=termTL_link)
