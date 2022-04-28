FROM python:3.9

ENV POSTGRESQL_HOST="localhost"
ENV POSTGRESQL_DATABASENAME="get_livros"
ENV POSTGRESQL_USER="crawler"
ENV POSTGRESQL_PASSWORD="crawler"
ENV POSTGRESQL_PORT="5432"

WORKDIR /code

COPY . /code

COPY ./requirements.txt requirements.txt

RUN  pip3 install --no-cache-dir --upgrade requirements.txt

CMD python main.py