from typing import Union
from pathlib import Path
from datetime import datetime, time
import random
import json
import re
import string
import requests
from wanakana import is_katakana, to_hiragana
from pydantic import BaseModel

from typing import Annotated
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
import starlette.status as status
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from fastapi.middleware.cors import CORSMiddleware

from . import models

from sqlmodel import Session, select, col
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import func

from . import secrets

from fastapi_htmx import htmx, htmx_init

def strip_punc(text):
    return ' '.join(word.strip(string.punctuation) for word in text.split())

def strip_punc_and_space(text):
    return ''.join(word.strip(string.punctuation) for word in text.split())

def letter_sub(letter):
    if letter == "~":
        return ["~"]
    elif letter == "あ":
        return ["あ", "い", "う", "え", "お"]    
    elif letter == "か":
        return ["か", "き", "く", "け", "こ"]  
    elif letter == "が":
        return ["が", "ぎ", "ぐ", "げ", "ご"]  
    elif letter == "さ":
        return ["さ", "し", "す", "せ", "そ"]  
    elif letter == "ざ":
        return ["さ", "じ", "ぢ", "ず", "ぜ", "ぞ"]  
    elif letter == "た":
        return ["た", "つ", "て", "と"]  
    elif letter == "だ":
        return ["だ", "ぢ", "づ", "で", "ど"]  
    elif letter == "な":
        return ["な", "に", "ぬ", "ね", "の"]  
    elif letter == "は":
        return ["は", "ひ", "ふ", "へ", "ほ"]  
    elif letter == "ば":
        return ["ば", "び", "ぶ", "べ", "ぼ"] 
    elif letter == "ぱ":
        return ["ぱ", "ぴ", "ぷ", "ぺ", "ぽ"]  
    elif letter == "ま":
        return ["ま", "み", "む", "め", "も"]  
    elif letter == "や":
        return ["や", "ゆ", "よ"]  
    elif letter == "ら":
        return ["ら", "り", "る", "れ", "ろ"]  
    elif letter == "わ":
        return ["わ"]
    else:
        return


app = FastAPI()

BASE_PATH = Path(__file__).resolve().parent

app.mount("/css", StaticFiles(directory=str(BASE_PATH /"css")), name="css")
app.mount("/root", StaticFiles(directory=str(BASE_PATH /"root")), name="root")
app.mount("/js", StaticFiles(directory=str(BASE_PATH /"js")), name="js")
app.mount("/media", StaticFiles(directory=str(BASE_PATH /"media")), name="media")
app.mount("/images", StaticFiles(directory=str(BASE_PATH /"images")), name="images")
app.mount("/sass", StaticFiles(directory=str(BASE_PATH /"sass")), name="sass")
app.mount("/fonts", StaticFiles(directory=str(BASE_PATH /"fonts")), name="fonts")

templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))

## PostgreSQL
url = "postgresql+psycopg://{}:{}@{}:{}/test_db".format(secrets.secrets['USER'], secrets.secrets['PASS'], secrets.secrets['IP_ADDRESS'], secrets.secrets['PORT'])
engine = models.create_engine(url)


def create_db_and_tables():
    models.SQLModel.metadata.create_all(engine)

async def search(search_term, offset=0, limit=10):
    matches = []
    with Session(engine) as session:
        # Search LIKE
        statement = select(models.Terms).where(col(models.Terms.name).contains(search_term)).offset(offset).limit(limit)
        results = session.exec(statement)
        all_results = results.all()

        if len(all_results) == 0:
            return None
        else:
            for terms in all_results:
                terms_tl = []
                results_as_dict = dict(terms)
                for items in terms.tl:
                    tl = dict(items)
                    terms_tl.append(tl)
                results_as_dict |= {"tl" : terms_tl}
                matches.append(results_as_dict)
            return matches

def get_term_count():
    with Session(engine) as session:
        statement = select(models.Terms)
        rows = session.exec(statement)
        return(len(rows.all()))

def get_def_count():
    defs = 0
    with Session(engine) as session:
        statement = select(models.Terms)
        result = session.exec(statement).all()
        for terms in result:
            defs += len(terms.tl)
        return defs

create_db_and_tables()

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/", response_class=HTMLResponse)
async def root_page(request: Request):
    match = {}
    time = datetime.now()
    length = get_term_count()
    defcount = get_def_count()
    date = time.strftime("%B %d, %Y")
    random.seed(int(time.day) * int(time.month) * int(time.year) * length)
    rand = round(random.random() * length)

    with Session(engine) as session:
        statement = select(models.Terms).where(models.Terms.id == rand)
        results = session.exec(statement)

        all_results = results.one()
        terms_tl = []
        results_as_dict = dict(all_results)
        for items in all_results.tl:
            tl = dict(items)
            terms_tl.append(tl)
            results_as_dict |= {"tl" : terms_tl}
        match = results_as_dict

    return templates.TemplateResponse(
        request=request, name="term_of_the_day.html", context={"date" : date, "term" : match, "length" : length, "defcount" : defcount}
    )


@app.get("/search/{term_id}", response_class=HTMLResponse)
async def search(request: Request, term_id: str):
    length = get_term_count()
    defcount = get_def_count()

    if term_id == "":
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        search_term = term_id if not is_katakana(term_id) else to_hiragana(term_id)

    matches = []
    found = False
    with Session(engine) as session:
        # Search LIKE
        statement = select(models.Terms).where(col(models.Terms.name).contains(search_term)).offset(0).limit(10)
        results = session.exec(statement)
        temp_results = results.all()
        if len(temp_results) > 0:
            found = True

        if not found:
            statement = select(models.Terms).where(col(models.Terms.romakana).contains(search_term)).offset(0).limit(10)
            results = session.exec(statement)
            temp_results = results.all()
            if len(temp_results) > 0:
                found = True
        
        if not found:
            statement = select(models.Terms).where(col(models.Terms.hepburn).contains(search_term)).offset(0).limit(10)
            results = session.exec(statement)
            temp_results = results.all()
            if len(temp_results) > 0:
                found = True
        
        if not found:
            statement = select(models.Terms).where(col(models.Terms.kunrei).contains(search_term)).offset(0).limit(10)
            results = session.exec(statement)
            temp_results = results.all()
            if len(temp_results) > 0:
                print("FOUND")
                found = True

        if not found:
            statement = select(models.Terms).where(col(models.Terms.nihon).contains(search_term)).offset(0).limit(10)
            results = session.exec(statement)
            temp_results = results.all()
            if len(temp_results) > 0:
                found = True
        
        if not found:
            statement = select(models.Terms).where(col(models.Terms.hepburn).contains(search_term)).offset(0).limit(10)
            results = session.exec(statement)
            temp_results = results.all()
            print(len(temp_results))
            if len(temp_results) > 0:
                found = True
        
        if not found:
            statement = select(models.Terms).where(col(models.Terms.lit).contains(search_term)).offset(0).limit(10)
            results = session.exec(statement)
            temp_results = results.all()
            if len(temp_results) > 0:
                found = True
        
        if not found:
            statement = select(models.Terms).where(col(models.Terms.altsearch).contains(search_term)).offset(0).limit(10)
            results = session.exec(statement)
            temp_results = results.all()
            if len(temp_results) > 0:
                found = True
        
        all_results = temp_results
        for terms in all_results:
            terms_tl = []
            results_as_dict = dict(terms)
            for items in terms.tl:
                tl = dict(items)
                terms_tl.append(tl)
            results_as_dict |= {"tl" : terms_tl}
            matches.append(results_as_dict)
            matches.sort(key=lambda k: k['name'])
            
    # print(matches)

    return templates.TemplateResponse(
        request=request, name="search.html", context={"terms" : matches, "length" : length, "defcount" : defcount}
    )

@app.get("/random", response_class=HTMLResponse)
async def search(request: Request):
    matches = []
    length = get_term_count()
    defcount = get_def_count()

    with Session(engine) as session:
        statement = select(models.Terms).order_by(func.random()).limit(20)
        results = session.exec(statement)

        all_results = results.all()
        for terms in all_results:
            terms_tl = []
            results_as_dict = dict(terms)
            for items in terms.tl:
                tl = dict(items)
                terms_tl.append(tl)
            results_as_dict |= {"tl" : terms_tl}
            matches.append(results_as_dict)

    return templates.TemplateResponse(
        request=request, name="search.html", context={"terms" : matches, "length" : length, "defcount" : defcount}
    )


@app.get("/add", response_class=HTMLResponse)
async def add(request: Request):
    return templates.TemplateResponse(
        request=request, name="add.html"
    )

class FormData(BaseModel):
    term: str
    definition: str
    cap_token: str

@app.post("/submit/", response_class=HTMLResponse)
# async def submit_term(term: Annotated[str, Form()], description: Annotated[str, Form()], cap-token: Annotated[str, Form()]):
async def submit_term(request: Request, submit: Annotated[FormData, Form()]):
    print("POST")
    print(submit.cap_token)
    url = 'https://cap.yamaguchi.duckdns.org/57a0c3bc6df0/siteverify'
    myobj = {'secret': '26490bcf3b1f906bd1e51f89c47955f8f51e2a1a04a18529d2', 'response': submit.cap_token}
    headers = {"Content-Type" : "application/json"}
    x = requests.post(url, json=myobj, headers=headers)
    print(x.text)
    return templates.TemplateResponse(
        request=request, name="submit.html"
    )

@app.get("/numbers", response_class=HTMLResponse)
async def search(request: Request):
    length = get_term_count()
    defcount = get_def_count()

    search_string = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    matches = []
    for number in search_string:
        # print(letters)
        with Session(engine) as session:
            # Search LIKE
            statement = select(models.Terms).where(col(models.Terms.romakana).istartswith(number))
            results = session.exec(statement)

            all_results = results.all()
            for terms in all_results:
                terms_tl = []
                results_as_dict = dict(terms)
                for items in terms.tl:
                    tl = dict(items)
                    terms_tl.append(tl)
                results_as_dict |= {"tl" : terms_tl}
                matches.append(results_as_dict)
    
    matches.sort(key=lambda k: k['romakana'])
    return templates.TemplateResponse(
        request=request, name="search.html", context={"terms" : matches, "length" : length, "defcount" : defcount}
    )
    

@app.get("/l/{letter}", response_class=HTMLResponse)
async def search(request: Request, letter: str):
    length = get_term_count()
    defcount = get_def_count()
    search_string = letter_sub(letter)
    if not search_string:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    matches = []
    for letters in search_string:
        # print(letters)
        with Session(engine) as session:
            # Search LIKE
            statement = select(models.Terms).where(col(models.Terms.romakana).istartswith(letters))
            results = session.exec(statement)

            all_results = results.all()
            for terms in all_results:
                terms_tl = []
                results_as_dict = dict(terms)
                for items in terms.tl:
                    tl = dict(items)
                    terms_tl.append(tl)
                results_as_dict |= {"tl" : terms_tl}
                matches.append(results_as_dict)
    
    matches.sort(key=lambda k: k['romakana'])
    return templates.TemplateResponse(
        request=request, name="search.html", context={"terms" : matches, "length" : length, "defcount" : defcount}
    )

@app.get("/new", response_class=HTMLResponse)
async def search(request: Request):
    matches = []
    length = get_term_count()
    defcount = get_def_count()

    with Session(engine) as session:
        statement = select(models.Terms).order_by(models.Terms.id.desc()).limit(30)
        results = session.exec(statement)

        all_results = results.all()
        for terms in all_results:
            terms_tl = []
            results_as_dict = dict(terms)
            for items in terms.tl:
                tl = dict(items)
                terms_tl.append(tl)
            results_as_dict |= {"tl" : terms_tl}
            matches.append(results_as_dict)

    return templates.TemplateResponse(
        request=request, name="search.html", context={"terms" : matches, "length" : length, "defcount" : defcount}
    )

@app.get("/print", response_class=HTMLResponse)
async def search(request: Request):
    matches = []

    with Session(engine) as session:
        statement = select(models.Terms).order_by(models.Terms.romakana)
        results = session.exec(statement)

        all_results = results.all()
        for terms in all_results:
            terms_tl = []
            results_as_dict = dict(terms)
            for items in terms.tl:
                tl = dict(items)
                terms_tl.append(tl)
            results_as_dict |= {"tl" : terms_tl}
            matches.append(results_as_dict)
    return templates.TemplateResponse(
        request=request, name="print.html", context={"terms" : matches}
    )


@app.get("/about", response_class=HTMLResponse)
async def get_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="about.html"
    )

@app.get("/about.html", response_class=HTMLResponse)
async def get_page(request: Request):
    return RedirectResponse(url="/about", status_code=status.HTTP_301_MOVED_PERMANENTLY)

@app.get("/resources", response_class=HTMLResponse)
async def get_page(request: Request):
    with open(str(BASE_PATH /"json/resources.json"), "r", encoding="utf8") as file:
        resources = json.load(file)
        return templates.TemplateResponse(
            request=request, name="resources.html", context={"resources" : resources}
        )

@app.get("/resources.html", response_class=HTMLResponse)
async def get_page(request: Request):
    return RedirectResponse(url="/resources", status_code=status.HTTP_301_MOVED_PERMANENTLY)
        

@app.get("/robots.txt", response_class=HTMLResponse)
async def get_page(request: Request):
    return FileResponse(BASE_PATH /"root/robots.txt")

@app.get("/sitemap.xml", response_class=HTMLResponse)
async def get_page(request: Request):
    return FileResponse(BASE_PATH /"root/sitemap.xml")

@app.get("/status")
async def health_check():
    return {"status" : "OK"}
