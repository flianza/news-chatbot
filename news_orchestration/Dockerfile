FROM prefecthq/prefect:2-python3.11

COPY requirements.txt .
RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir

COPY flows /opt/prefect/flows
COPY news_dbt /news_dbt