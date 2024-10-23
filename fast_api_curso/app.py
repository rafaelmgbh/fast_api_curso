from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_api_curso.routers import auth, todo, users

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todo.router)


@app.get("/", status_code=HTTPStatus.OK)
def read_root():
    return {"Hello": "World"}


@app.get("/html", response_class=HTMLResponse)
def read_html():
    return """
    <html>
        <head>
            <title>Este e o Retorno da Requisição</title>
        </head>
        <body>
            <h1>Olá Mundo</h1>
        </body>
    """
