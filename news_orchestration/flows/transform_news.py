import time
from typing import Any, Sequence

import chromadb
from chromadb.config import Settings
from config import CHAT_MODEL, CHROMA_DB_COLLECTION, CHROMA_DB_PORT, CHROMA_DB_SERVER, EMBEDDINGS_MODEL, OLLAMA_URL
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from prefect import flow, task
from prefect_dbt.cli.commands import DbtCoreOperation
from sqlalchemy import create_engine, sql


@task
def create_embeddings() -> None:
    engine = create_engine("postgresql+psycopg2://news:news@db/news")
    with engine.connect() as conn:
        str_sql = sql.text("select * from public_staging.news")
        rows = conn.execute(str_sql).fetchall()

    documents = []
    for row in rows:
        document = Document(
            row.title,
            metadata={
                "published": time.mktime(row.published.timetuple()),
            },
        )
        documents.append(document)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    all_splits = text_splitter.split_documents(documents)

    oembed = OllamaEmbeddings(
        base_url=OLLAMA_URL,
        model=EMBEDDINGS_MODEL,
    )
    chroma_client = chromadb.HttpClient(
        host=CHROMA_DB_SERVER,
        port=CHROMA_DB_PORT,
        settings=Settings(allow_reset=True, anonymized_telemetry=False),
    )
    chroma_client.reset()
    Chroma.from_documents(
        client=chroma_client,
        documents=all_splits,
        embedding=oembed,
        collection_name=CHROMA_DB_COLLECTION,
    )


def run_dbt_commands(commands: Sequence[str], prev_task_result: Any) -> DbtCoreOperation:
    dbt_task = DbtCoreOperation(
        commands=commands,
        project_dir="/news_dbt",
        wait_for=prev_task_result,
    )
    return dbt_task


@flow(log_prints=True)
def transform_news() -> None:
    # run dbt precheck
    dbt_init_task = task(
        name="dbt Precheck",
        log_prints=True,
    )(run_dbt_commands)(
        commands=["dbt debug", "dbt list"],
        prev_task_result=None,
    )
    dbt_init_task.run()

    # run dbt models
    dbt_run_task = task(
        name="Transform with dbt",
        log_prints=True,
    )(run_dbt_commands)(
        commands=["dbt run"],
        prev_task_result=dbt_init_task,
    )
    dbt_run_task.run()

    # create embeddings
    create_embeddings(wait_for=dbt_run_task)


if __name__ == "__main__":
    transform_news.serve(name="transform-news")
