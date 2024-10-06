from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK)
def read_root():
    return {"Hello": "World"}


@app.get("/html", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>Este e o Retorno da Requisição</title>
        </head>
        <body>
            <h1>Olá Mundo</h1>
        </body>
    """
