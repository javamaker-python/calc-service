from fastapi.applications import FastAPI
import uvicorn

from calc import calculator_api

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

if __name__ == '__main__':
    uvicorn.run("main:app", host = "127.0.0.1", port = 8000, reload = True)
    pass
