from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import pandas as pd
from datetime import datetime

livros = []

def cria_html(url_index):
    response = urlopen(url_index)

    html = response.read()

    return html.decode('utf-8')


def trata_html(html):
    return " ".join(html.split()).replace('> <', '><')


# Captura as categorias/links dos livros
def categorias():
    html = cria_html('https://books.toscrape.com/index.html')

    html = trata_html(html)

    soup = BeautifulSoup(html, 'html.parser')

    informacoes = soup.find(
        'ul', class_='nav-list').find('ul').findAll('a')

    categorias = {}

    for informacao in informacoes:
        categorias[" ".join(informacao.get_text().split()).lower()] = 'https://books.toscrape.com/'+informacao.get('href')
   
    return categorias


def crawler(categoria):
    if categorias().get(categoria) != None:

        category = str(categorias().get(categoria)).split('/')[-2]

        html = cria_html(
            'https://books.toscrape.com/catalogue/category/books/'+category+'/index.html')

        html = trata_html(html)

        soup = BeautifulSoup(html, 'html.parser')

        pages = soup.find('li', class_='current')

        link_livros = []

        if pages is None:

            links = soup.find('ol', class_='row').findAll('h3')

            for link in links:
                link_livros.append('https://books.toscrape.com/catalogue/' +
                                    str(link).split('"')[1].split('../../../')[-1])

        else:
            link_livros = []

            for i in range(int(pages.get_text().split()[-1])):

                html = cria_html(
                    'https://books.toscrape.com/catalogue/category/books/'+category+'/page-' + str(i + 1)+'.html')

                html = trata_html(html)

                soup = BeautifulSoup(html, 'html.parser')

                links = soup.find('ol', class_='row').findAll('h3')

                for link in links:
                    link_livros.append(
                        'https://books.toscrape.com/catalogue/'+str(link).split('"')[1].split('../../../')[-1])

        for link in link_livros:

            html = cria_html(link)

            html = trata_html(html)

            soup = BeautifulSoup(html, 'html.parser')

            livro = {}


            livro['Titulo'] = soup.find(
                'div', class_='product_main').find('h1').get_text()
            livro['Preco'] = soup.find(
                'div', class_='product_main').find('p').get_text()
            livro['Estoque'] = int(soup.find('div', class_='product_main').find(
                'p', class_='instock availability').get_text().split('(')[-1].split(' ')[0])
            livro['Descricao'] = soup.find(
                'article', class_='product_page').find('p', class_='').get_text()
            livro['Data_de_crawleamento'] = datetime.now().strftime('%d/%m/%Y')

            livros.append(livro)

        JS_livros = {}

        JS_livros[categoria] = livros

        JS_livros = json.dumps(JS_livros)

        return livros
    
    else:
        return {"category": "Not Found"}
