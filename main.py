import json
from turtle import st
import pandas as pd

from fastapi import FastAPI
from crawler import crawler
from db import *

app = FastAPI()
criar_schema()

@app.post("/salvar-livros/{categoria}")
def get_livros_bd(categoria:str):
    dados = crawler(categoria)
    print(dados)
    if type(dados) is list:
        df = pd.DataFrame(dados)

        inserir_dados_tabela(df, categoria)
    
    elif type(dados) is dict:
        return dados



@app.get("/retorna-livros-quantidade/{categoria}/{quantidade}")
def save_livros_crawler(categoria:str, quantidade):
    return retorna_n_livros(categoria, quantidade)


@app.get("/retorna-livros-quantidade_inferior/{categoria}/{quantidade}")
def get_livros_estoque_baixo_bd(categoria: str, quantidade):
    return retorna_livros_com_quantidade_inferior(categoria, quantidade)


@app.post("/delete-livros/{categoria}")
def delete_livros_bd(categoria):
    apagar_tabela(categoria)
