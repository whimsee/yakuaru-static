from typing import Union
from pathlib import Path
from datetime import datetime, time
import random
import json
import re
import requests
from pydantic import BaseModel

import cutlet
import string
import wanakana
import pykakasi

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

def generate_furigana(text):
    temp = ""
    result = kks.convert(text)
    for item in result:
        temp += item['hira']
    return temp

cutlet_hepburn = cutlet.Cutlet(use_foreign_spelling=False)
cutlet_kunrei = cutlet.Cutlet(system="kunrei",use_foreign_spelling=False)
cutlet_nihon = cutlet.Cutlet(system="nihon",use_foreign_spelling=False)

kks = pykakasi.kakasi()

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
        search_term = term_id if not wanakana.is_katakana(term_id) else wanakana.to_hiragana(term_id)

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
    kana: str
    literal: str
    definition: str
    explanation: str
    source: str
    jpsam: str
    ensam: str
    contributor: str
    cap_token: str

@app.post("/submit/", response_class=HTMLResponse)
async def submit_term(request: Request, submit: Annotated[FormData, Form()]):
    ADD_TERM = False
    TERM_FOUND = False
    DEF_FOUND = False
    url = 'https://cap.yamaguchi.duckdns.org/' + secrets.secrets['CAP_API'] + '/siteverify'
    myobj = {'secret': secrets.secrets['CAP_SECRET'], 'response': submit.cap_token}
    headers = {"Content-Type" : "application/json"}
    x = requests.post(url, json=myobj, headers=headers)
    # print(type(x.text))
    cap_result = json.loads(x.text)
    print(submit)
    print(cap_result)
    # print(term, description)

    if "error" in cap_result:
        return templates.TemplateResponse(
            request=request, name="error.html", context={"error" : "Invalid Captcha. Try submitting again."}
        )


    try:
        if cap_result['success'] == True:
            ADD_TERM = True
        else:
            return templates.TemplateResponse(
                request=request, name="error.html", context={"error" : "Invalid Captcha. Try submitting again."}
            )
    except KeyError:
        return templates.TemplateResponse(
            request=request, name="error.html", context={"error" : "Invalid Captcha. Try submitting again."}
        )

    # try:
    #     if cap_result['success'] == True:
    #         return templates.TemplateResponse(
    #             request=request, name="submit.html"
    #         )
    #     else:
    #         return templates.TemplateResponse(
    #             request=request, name="error.html", context={"error" : "Invalid Captcha. Try submitting again."}
    #         )
    # except KeyError:
    #     return templates.TemplateResponse(
    #         request=request, name="error.html", context={"error" : "Invalid Captcha. Try submitting again."}
    #     )

    term = submit.term
    kana = submit.kana

    if not wanakana.is_hiragana(kana):
        if wanakana.is_katakana(kana):
            kana = wanakana.to_hiragana(kana)
        else:
            return templates.TemplateResponse(
                request=request, name="error.html", context={"error" : "KANA field must be in hiragana or katakana"}
            )

    hepburn = cutlet_hepburn.romaji(kana).replace(" ","").lower();
    kunrei = cutlet_kunrei.romaji(kana).replace(" ","").lower();
    nihon = cutlet_nihon.romaji(kana).replace(" ","").lower();

    for token in term:
        if wanakana.is_kanji(token):
            furigana = kana
            break
        else:
            furigana = None

    lit = submit.literal
    definition = submit.definition
    explanation = submit.explanation
    source = submit.source
    jpsam = submit.jpsam
    ensam = submit.ensam
    contributor = submit.contributor

    altsearch = strip_punc_and_space(definition) + (wanakana.to_hiragana(term) if wanakana.is_katakana(term) else kana) + hepburn

    print(hepburn, kunrei, nihon)
    print(furigana)
    print(kana)

    with Session(engine) as session:
        statement = select(models.Terms).where(models.Terms.name == term)
        try:
            one_result = session.exec(statement).one()
            TERM_FOUND = True
            print("TERM FOUND")
            print(one_result.id)
        except NoResultFound:
            print("No result")

        if TERM_FOUND:
            statement = select(models.TL).where(models.TL.definition == definition)
            try:
                one_result = session.exec(statement).one()
                DEF_FOUND = True
                print("DEF FOUND")
                print(one_result.id)
            except NoResultFound:
                print("No result")

        if TERM_FOUND and DEF_FOUND:
            return templates.TemplateResponse(
                request=request, name="error.html", context={"error" : "TERM and DEFINITION already exists"}
            )

        if ADD_TERM:
            return templates.TemplateResponse(
                    request=request, name="submit.html"
                )

        # print(defs)
        definition = get_tl(defs, "def")
        defexp = get_tl(defs, "defexp")
        source_temp = get_tl(defs, "src")
        jpsam = get_tl(defs, "jpsam")
        ensam = get_tl(defs, "ensam")
        # credit_temp = get_tl(defs, "credit")
        credit = get_tl(defs, "credit")

        ### Create altsearch
        altsearch += strip_punc_and_space(definition)

        if defexp != None:
            altsearch += strip_punc_and_space(defexp)

        ### Prep source. convert list to string with separator
        if source_temp != None:
            if POSTGRES:
                source = source_temp
            elif POSTGRES == False and isinstance(source_temp, list):
                source = "^*".join(str(x) for x in source_temp)
            else:
                source = source_temp
        else:
            source = None

        ### Prep credit. convert list to string with separator
        # if credit_temp != None:
        #     if POSTGRES:
        #         credit = credit_temp
        #     elif POSTGRES == False and isinstance(credit_temp, list):
        #         credit = "^*".join(str(x) for x in credit_temp)
        #     else:
        #         credit = credit_temp
        # else:
        #     credit = None


        ### each img
        # check if img exists and set parameters
        img = get_tl(defs, "img")
        if img != None:
            img_format = img[0]
            img_caption = img[1]
            # try:
            #     img_caption = img[1]
            # except IndexError:
            #     img_caption = None
        else:
            img_format = None
            img_caption = None

        tl_add = TL(
                        definition=definition,
                        defexp=defexp,
                        src=source,
                        credit=credit,
                        jpsam=jpsam,
                        ensam=ensam,
                        image_format=img_format,
                        image_caption=img_caption,
                    )

        TL_TERMS.append(tl_add)

        term_add = Terms(
                    name=term,
                    altterm=altterm,
                    romakana=romakana,
                    lit=lit,
                    hepburn=hepburn,
                    kunrei=kunrei,
                    nihon=nihon,
                    furigana=furigana,
                    kanaoverride=kanaoverride,
                    altsearch=altsearch,
                    tl=TL_TERMS
                )

        print("Adding:", term)
        session.add(term_add)
        session.commit()
    # return {"message": "Hello World"}

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
