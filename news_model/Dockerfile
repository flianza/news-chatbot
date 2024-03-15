FROM python:3.11-slim-bookworm

ARG UID=1000
ARG GID=1000

WORKDIR /api

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl \
    && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
    && apt-get clean \
    && groupadd -g "${GID}" python \
    && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" python \
    && chown python:python -R /api

USER python

ENV PYTHONUNBUFFERED="true" \
    PYTHONPATH="." \
    PATH="${PATH}:/home/python/.local/bin" \
    USER="python"

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --user --upgrade -r ./requirements.txt

COPY ./app ./app

EXPOSE 80

CMD ["uvicorn", "app.server:create_app", "--factory", "--host", "0.0.0.0", "--port", "80", "--reload"]