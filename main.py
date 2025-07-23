from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import uvicorn

from calc import calculator_api
from calc.api_respone import ValueErrorDetail

app = FastAPI(
    title = "Calculator API",
    description = "Простой REST-сервис для выполнения арифметических операций.",
    version = "1.0.0"
)

app.include_router(
    calculator_api.router,
    prefix = "/calculator",
    tags = ["calculator"]
)

# Регистрация обработчика для ValueError
@app.exception_handler(ValueError)
async def value_error_exception_handler(_: Request, exc: ValueError):
    """
    Этот обработчик будет "ловить" все исключения ValueError,
    которые не были перехвачены ранее в коде.
    """
    error_detail = ValueErrorDetail.of(exc)
    return JSONResponse(
        status_code = status.HTTP_400_BAD_REQUEST,
        content = error_detail.model_dump()
    )

if __name__ == '__main__':
    uvicorn.run("main:app", host = "127.0.0.1", port = 8000, reload = True)
    pass
