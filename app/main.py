from typing import Union
from pathlib import Path
from datetime import datetime, time
import random
import json
import re
import string
from wanakana import is_katakana, to_hiragana

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
import starlette.status as status
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from fastapi.middleware.cors import CORSMiddleware

from fastapi_htmx import htmx, htmx_init

def strip_punc(text):
    return ' '.join(word.strip(string.punctuation) for word in text.split())

def strip_punc_and_space(text):
    return ''.join(word.strip(string.punctuation) for word in text.split())

def letter_sub(letter):
    if letter == "~":
        return r"[~]"
    elif letter == "あ":
        return r"\b[あいうえお]"
    elif letter == "か":
        return r"\b[かきくけこ]"
    elif letter == "が":
        return r"\b[がぎぐげご]"
    elif letter == "さ":
        return r"\b[さしすせそ]"
    elif letter == "ざ":
        return r"\b[さじぢずぜぞ]"
    elif letter == "た":
        return r"\b[たつてと]"
    elif letter == "だ":
        return r"\b[だぢづでど]"
    elif letter == "な":
        return r"\b[なにぬねの]"
    elif letter == "は":
        return r"\b[はひふへほ]"
    elif letter == "ば":
        return r"\b[ばびぶべぼ]"
    elif letter == "ぱ":
        return r"\b[ぱぴぷぺぽ]"
    elif letter == "ま":
        return r"\b[まみむめも]"
    elif letter == "や":
        return r"\b[やゆよ]"
    elif letter == "ら":
        return r"\b[らりるれろ]"
    elif letter == "わ":
        return r"\b[わ]"
    else:
        return

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

app = FastAPI()

# origins = [
#     "https://test2.yamaguchi.duckdns.org",
#     "http://test2.yamaguchi.duckdns.org",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
#     max_age=3600,
# )

BASE_PATH = Path(__file__).resolve().parent

app.mount("/css", StaticFiles(directory=str(BASE_PATH /"css")), name="css")
app.mount("/root", StaticFiles(directory=str(BASE_PATH /"root")), name="root")
app.mount("/js", StaticFiles(directory=str(BASE_PATH /"js")), name="js")
app.mount("/media", StaticFiles(directory=str(BASE_PATH /"media")), name="media")
app.mount("/images", StaticFiles(directory=str(BASE_PATH /"images")), name="images")
app.mount("/sass", StaticFiles(directory=str(BASE_PATH /"sass")), name="sass")
app.mount("/fonts", StaticFiles(directory=str(BASE_PATH /"fonts")), name="fonts")

templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/", response_class=HTMLResponse)
async def root_page(request: Request):
    time = datetime.now()
    defcount = 0
    length = 0
    date = time.strftime("%B %d, %Y")
    with open(str(BASE_PATH /"json/glossaryMaster.json"), "r", encoding="utf8") as file:
        data = json.load(file)
        length = int(len(data))
        for x in data.keys():
            defcount += len(data[x]['tl'])
        random.seed(int(time.day) * int(time.month) * int(time.year) * length)
        rand = round(random.random() * length)
        term_index = list(data)[rand]
        term = data[term_index]
    return templates.TemplateResponse(
        request=request, name="term_of_the_day.html", context={"date" : date, "term" : term, "length" : length, "defcount" : defcount}
    )


@app.get("/search/{term_id}", response_class=HTMLResponse)
async def search(request: Request, term_id: str):
    terms = []
    length = 0
    defcount = 0
    if term_id == "":
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        search_term = term_id if not is_katakana(term_id) else to_hiragana(term_id)
    with open(str(BASE_PATH /"json/glossaryMaster.json"), "r", encoding="utf8") as file:
        data = json.load(file)
        length = int(len(data))
        for x in data.keys():
            defcount += len(data[x]['tl'])
        terms = await term_search(data, search_term)
    return templates.TemplateResponse(
        request=request, name="search.html", context={"terms" : terms, "length" : length, "defcount" : defcount}
    )

@app.get("/random", response_class=HTMLResponse)
async def search(request: Request):
    terms = []
    length = 0
    defcount = 0
    iterations = 0
    with open(str(BASE_PATH /"json/glossaryMaster.json"), "r", encoding="utf8") as file:
        data = json.load(file)
        length = int(len(data))
        for x in data.keys():
            defcount += len(data[x]['tl'])
        for term in data.values():
            if iterations == 20:
                break
            else:
                terms.append(term)
                iterations += 1
        random.shuffle(terms)
    return templates.TemplateResponse(
        request=request, name="search.html", context={"terms" : terms, "length" : length, "defcount" : defcount}
    )

@app.get("/numbers", response_class=HTMLResponse)
async def search(request: Request):
    terms = []
    length = 0
    defcount = 0
    with open(str(BASE_PATH /"json/glossaryMaster.json"), "r", encoding="utf8") as file:
        data = json.load(file)
        length = int(len(data))
        for x in data.keys():
            defcount += len(data[x]['tl'])
        terms = await term_search(data, "[1234567890]")
    return templates.TemplateResponse(
        request=request, name="search.html", context={"terms" : terms, "length" : length, "defcount" : defcount}
    )

@app.get("/l/{letter}", response_class=HTMLResponse)
async def search(request: Request, letter: str):
    search_string = letter_sub(letter)
    if not search_string:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    terms = []
    length = 0
    defcount = 0
    with open(str(BASE_PATH /"json/glossaryMaster.json"), "r", encoding="utf8") as file:
        data = json.load(file)
        length = int(len(data))
        for x in data.keys():
            defcount += len(data[x]['tl'])
        terms = await term_search(data, search_string, True)
    return templates.TemplateResponse(
        request=request, name="search.html", context={"terms" : terms, "length" : length, "defcount" : defcount}
    )

@app.get("/new", response_class=HTMLResponse)
async def search(request: Request):
    terms = []
    length = 0
    defcount = 0
    iterations = 0
    with open(str(BASE_PATH /"json/glossaryMaster.json"), "r", encoding="utf8") as file:
        data = json.load(file)
        length = int(len(data))
        for x in data.keys():
            defcount += len(data[x]['tl'])
        for term in reversed(data.values()):
            if iterations == 20:
                break
            else:
                terms.append(term)
                iterations += 1
    return templates.TemplateResponse(
        request=request, name="search.html", context={"terms" : terms, "length" : length, "defcount" : defcount}
    )

@app.get("/print", response_class=HTMLResponse)
async def search(request: Request):
    terms = []
    with open(str(BASE_PATH /"json/glossaryMaster.json"), "r", encoding="utf8") as file:
        data = json.load(file)
        length = int(len(data))
        for term in reversed(data.values()):
            terms.append(term)
        terms.sort(key=lambda k: k['term'])
    return templates.TemplateResponse(
        request=request, name="print.html", context={"terms" : terms}
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
