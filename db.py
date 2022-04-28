from fastapi import Query
import pandas as pd
from requests import session
from sqlalchemy import create_engine
import sqlalchemy


def criar_engine():
    DATABASE_URL = "postgresql+psycopg2://postgres:crawler@postgres:5432/postgres"
    engine = create_engine(DATABASE_URL)
    return engine


def criar_schema():
    engine = criar_engine()
    if not engine.dialect.has_schema(engine, 'livro'):
        criar_engine().execute(sqlalchemy.schema.CreateSchema('livro'))


def inserir_dados_tabela(dataframe, table_name):
    dataframe.to_sql(
        table_name,
        criar_engine(),
        schema='livro',
        if_exists="append",
        index=False,
        chunksize=10000
    )


def retorna_n_livros(categoria, quantidade):
    df = pd.read_sql_query(f'SELECT * FROM livro.{categoria} LIMIT {quantidade}', con=criar_engine())
    JS_livros = {}
    JS_livros[categoria] = df.to_dict('records')
    return JS_livros


def retorna_livros_com_quantidade_inferior(categoria, quantidade):
    df = pd.read_sql_query(f'SELECT * FROM livro.{categoria} where (SELECT COUNT(*) FROM livro.{categoria}) < {quantidade}', criar_engine())

    if not df.isnull().values.all():
        JS_livros = {}
        JS_livros[categoria] = df.to_dict('records')
        return JS_livros




def apagar_tabela(categoria):
    sql = (f'DROP TABLE IF EXISTS livro.{categoria}')
    criar_engine().execute(sql)

