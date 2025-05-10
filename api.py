from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dictionary import dictionary
import json

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 400:
        return JSONResponse(
            status_code=400,
            content={
                "error": "400 Bad Request",
                "message": "The request was invalid or cannot be served."
            }
        )
    elif exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={
                "error": "404 Not Found",
                "message": "Word not found!"
            }
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": f"{exc.status_code} Error",
            "message": exc.detail
        }
    )

@app.exception_handler(RateLimitExceeded)
async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "error": "429 Too Many Requests",
            "message": "You have exceeded the rate limit for requests."
        }
    )

@app.exception_handler(Exception)
async def internal_server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "500 Internal Server Error",
            "message": "An unexpected error occurred on the server."
        }
    )

# @app.get("/")
# def root(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})
@app.get("/v1")
@limiter.limit("100/minute")
def get_dictionary_index(request: Request):
    return JSONResponse(content={"message": "Welcome to the Dictionary API! Current version: v1.0.0, Check the documentation for usage."})

@app.get("/")
@limiter.limit("100/minute")
def get_index(request: Request):
    return JSONResponse(content={"message": "Welcome to the Dictionary API! Current version: v1.0.0, Check the documentation for usage."})

@app.get("/dictionary")
@limiter.limit("100/minute")
def get_dictionary_index(request: Request):
    return JSONResponse(content={"message": "Welcome to the Dictionary API! Current version: v1.0.0, Check the documentation for usage."})

@app.get("/dictionary/v1/{word}")
@limiter.limit("100/minute")
def get_dictionary(word: str, request: Request):
    word = word.lower()
    try:
        result = dictionary(word)
        if result is None:
            raise HTTPException(status_code=404, detail="Word not found!")
        return JSONResponse(content=json.loads(result))
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format.")
