from typing import Sequence

import chromadb
from app.config import CHAT_MODEL, CHROMA_DB_COLLECTION, CHROMA_DB_PORT, CHROMA_DB_SERVER, EMBEDDINGS_MODEL, OLLAMA_URL
from chromadb.config import Settings
from langchain.pydantic_v1 import BaseModel, Field
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

llm = ChatOllama(
    base_url=OLLAMA_URL,
    model=CHAT_MODEL,
    temperature=0,
    streaming=True,
)


def buscar_noticias(query: dict) -> Sequence[str]:
    import datetime as dt
    import time

    chroma_client = chromadb.HttpClient(
        host=CHROMA_DB_SERVER,
        port=CHROMA_DB_PORT,
        settings=Settings(allow_reset=True, anonymized_telemetry=False),
    )

    db = Chroma(
        client=chroma_client,
        embedding_function=OllamaEmbeddings(
            base_url=OLLAMA_URL,
            model=EMBEDDINGS_MODEL,
        ),
        collection_name=CHROMA_DB_COLLECTION,
    )

    fecha = query["fecha"].lower()
    if fecha == "ayer":
        fecha_dt = dt.datetime.today() - dt.timedelta(days=1)
    else:
        fecha_dt = dt.datetime.strptime(fecha, "%Y-%m-%d")
    fecha_unix = time.mktime(fecha_dt.timetuple())

    documents = db.similarity_search(
        query["tematica"],
        k=5,
        filter={"published": {"$gt": fecha_unix}},
    )

    if len(documents) > 0:
        return "\t- " + "\n\t- ".join([document.page_content for document in documents])
    return "\t- Sin noticias relevantes"


def _crear_chain_tematica(llm):
    template_tematica = """A partir de la pregunta del usuario, debes extraer la temática a la cual se refiere. Lo que importa es el sujeto, no adjetivos, fechas, etc.
Por ejemplo:
    - "qué pasó en Rio de Janeiro ayer?", la temática es "Rio de Janeiro"
    - "qué hiciste ayer en el centro de Rosario?", la temática es "centro de Rosario"
    - "cuantas plantas tiene tu casa?", la temática es "plantas de tu casa"
Solo debes responder el nombre de la temática ignorando el resto de la pregunta:

{input}
"""
    prompt_tematica = ChatPromptTemplate.from_template(template_tematica)

    chain_tematica = (
        RunnableParallel({"input": RunnablePassthrough()})
        | prompt_tematica
        | llm
        | StrOutputParser()
        | (lambda x: x.strip())
    )

    chain_tematica.name = "Tematica"
    return chain_tematica


def _crear_chain_fecha(llm):
    template_fecha = """A partir de la pregunta del usuario, debes extraer una fecha a la cual hace referencia.
Por ejemplo:
    - "qué vas a hacer mañana?", la fecha es "mañana"
    - "qué hiciste ayer?", la fecha es "ayer"
    - "qué hiciste el 1 de noviembre de 1990?", la fecha es "1990-11-01"
En caso de detectar una fecha especifica, devuelvela en formato "AAAA-MM-DD".
En caso de no estar seguro cuál es la fecha, responde "Ayer".∂

Solo debes responder la fecha que detectes:

{input}
"""
    prompt_fecha = ChatPromptTemplate.from_template(template_fecha)

    chain_fecha = (
        RunnableParallel({"input": RunnablePassthrough()})
        | prompt_fecha
        | llm
        | StrOutputParser()
        | (lambda x: x.strip())
    )

    chain_fecha.name = "Fecha"
    return chain_fecha


def _crear_chain_noticias(chain_tematica, chain_fecha):
    chain_noticias = (
        RunnableParallel(
            {
                "tematica": chain_tematica,
                "fecha": chain_fecha,
            }
        )
        | buscar_noticias
    )
    chain_noticias.name = "Noticias"
    return chain_noticias


class InputSchema(BaseModel):
    pregunta: str = Field()


def crear_chain():
    chain_tematica = _crear_chain_tematica(llm)
    chain_fecha = _crear_chain_fecha(llm)
    chain_noticias = _crear_chain_noticias(chain_tematica, chain_fecha)

    template = """A partir de la pregunta del usuario y las noticias que hablan de la temática del usuario elabora una respuesta a la pregunta.

{pregunta}

Noticias de la temática:
{contexto}
"""
    prompt = ChatPromptTemplate.from_template(template)

    chain = (
        RunnableParallel(
            {
                "contexto": chain_noticias,
                "pregunta": RunnablePassthrough(),
            }
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    chain.name = "Resumen noticias"

    return chain.with_types(input_type=InputSchema)
