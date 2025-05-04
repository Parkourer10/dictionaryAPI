from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from dictionary import dictionary
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/dictionary/{word}")
def get_dictionary(word: str):
    word = word.lower()
    result = dictionary(word)
    return JSONResponse(content=json.loads(result))
