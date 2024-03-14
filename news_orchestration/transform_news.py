import time
from typing import Any, Sequence

import chromadb
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from prefect import flow, task
from prefect_dbt.cli.commands import DbtCoreOperation
from sqlalchemy import create_engine, sql


def create_chroma_client():
    return chromadb.HttpClient(
        host="localhost",
        port=8500,
        settings=Settings(allow_reset=True, anonymized_telemetry=False),
    )


@task
def create_embeddings() -> None:
    engine = create_engine("postgresql+psycopg2://news:news@localhost/news")
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

    oembed = OllamaEmbeddings(model="openchat")
    chroma_client = create_chroma_client()
    chroma_client.reset()
    Chroma.from_documents(
        client=chroma_client,
        documents=all_splits,
        embedding=oembed,
        collection_name="news",
    )


def run_dbt_commands(commands: Sequence[str], prev_task_result: Any) -> DbtCoreOperation:
    dbt_task = DbtCoreOperation(
        commands=commands,
        project_dir="../dbt_news",
        wait_for=prev_task_result,
    )
    return dbt_task


@flow(log_prints=True)
def transform_news() -> None:
    # run dbt precheck
    dbt_init_task = task(name="dbt Precheck")(run_dbt_commands)(
        commands=["dbt debug", "dbt list"],
        prev_task_result=None,
    )
    dbt_init_task.run()

    # run dbt models
    dbt_run_task = task(name="Transform with dbt")(run_dbt_commands)(
        commands=["dbt run"],
        prev_task_result=dbt_init_task,
    )
    dbt_run_task.run()

    # create embeddings
    create_embeddings(wait_for=dbt_run_task)


if __name__ == "__main__":
    transform_news()
