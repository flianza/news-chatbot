from app.model import crear_chain
from fastapi import FastAPI
from langserve import add_routes


def create_app():
    app = FastAPI(
        title="LangChain Server",
        version="1.0",
        description="A simple api server using Langchain's Runnable interfaces",
    )

    add_routes(
        app,
        crear_chain(),
        path="/news",
    )

    return app
