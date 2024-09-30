from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
current_locale = locale.getlocale()

from . import router


origins = ["http://localhost:8081", "http://127.0.0.1:8081", "*"]

app = FastAPI(
    docs_url="/docs",
    title="CurrencyRateAPI",
    openapi_url="/api/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.exception_handler(RequestValidationError)
async def validation_request_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({ "error": exc.errors(), "body": exc.body })
    )

app.include_router(router.weatherapi.router)