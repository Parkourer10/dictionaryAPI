from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from dictionary import dictionary
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/dictionary/{word}")
@limiter.limit("500/minute") #500 reqs per min for an ip
def get_dictionary(word: str, request: Request):
    word = word.lower()
    result = dictionary(word)
    return JSONResponse(content=json.loads(result))