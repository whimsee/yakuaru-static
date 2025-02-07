from sqlmodel import SQLModel, create_engine, Field, Relationship, Column, String
import sqlalchemy

# class termTL_link(SQLModel, table=True):
#     term_id: int | None = Field(default=None, foreign_key="terms.id", primary_key=True)
#     tl_id: int | None = Field(default=None, foreign_key="tl.id", primary_key=True)



class Terms(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    altterm: str = Field(default=None, index=True)
    romakana: str = Field(index=True)
    lit: str | None = None
    hepburn: str | None = Field(default=None, index=True)
    kunrei: str | None = Field(default=None, index=True)
    nihon: str | None = Field(default=None, index=True)
    furigana: str | None = None
    # altsearch: str | None = Field(default=None, index=True)

    tl: None | list["TL"] = Relationship(back_populates="terms", cascade_delete=True)

class TL(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    definition: str = Field(index=True)
    defexp: str | None = None
    src: str | None = Field(default=None, index=True)
    credit: str | None = None
    jpsam: str | None = Field(default=None, index=True)
    ensam: str | None = Field(default=None, index=True)
    image_format: str | None = None
    image_caption: str | None = None

    term_id: int | None = Field(default=None, foreign_key="terms.id", ondelete="CASCADE")
    terms: Terms = Relationship(back_populates="tl")