#%%
# EXTRAÇÃO DOS LIVROS PUBLICADOS  
import os
import zipfile
import re
from bs4 import BeautifulSoup
import pandas as pd


def fun_result(result):
    """Função auxiliar para extrair conteúdo de expressões regulares."""
    return result.group(1) if result is not None else 'VAZIO'


def process_livros(directory, years):
    """Processa cada arquivo ZIP no diretório especificado, extrai e gera relatórios de livros publicados nos anos especificados."""
    global df_all_books
    df_all_books = pd.DataFrame()  # Reinicializa o DataFrame global para cada chamada de função

    for filename in os.listdir(directory):
        if filename.endswith(".zip"):
            zip_path = os.path.join(directory, filename)
            print(f"Processando {zip_path}...")
            df_current_books = getlivro(zip_path, years)
            df_all_books = pd.concat([df_all_books, df_current_books], ignore_index=True)

    # Exporta os dados acumulados para um único arquivo CSV
    output_dir = './LIVROS IMIP'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    all_books_path = f'{output_dir}/all_books_{",".join(map(str, years))}.csv'
    df_all_books.to_csv(all_books_path, index=False)
    print(f'Todos os dados de livros foram gravados em {all_books_path}')


def getlivro(zip_path, years):
    """Função para extrair informações de livros publicados ou organizados nos anos especificados."""
    with zipfile.ZipFile(zip_path, 'r') as archive:
        try:
            lattesxmldata = archive.open('curriculo.xml')
        except KeyError:
            print(f"curriculo.xml não encontrado em {zip_path}")
            return pd.DataFrame()  # Retorna um DataFrame vazio em caso de falha
        soup = BeautifulSoup(lattesxmldata, 'lxml', from_encoding='ISO-8859-1')

        # Extração dos dados dos livros
        livscaps = soup.find_all('livros-e-capitulos')
        if not livscaps:
            print(f'Livros publicados não encontrados para {zip_path}')
            return pd.DataFrame()

        # Estruturas para armazenar dados extraídos
        data = {
            'TITLE': [],
            'YEAR': [],
            'LANG': [],
            'EDITORA': [],
            'AUTHORS': []
        }

        for livpuborg in livscaps[0].find_all('livro-publicado-ou-organizado'):
            dbl = livpuborg.find_all('dados-basicos-do-livro')
            for item in dbl:
                year = fun_result(re.search('ano=\"(.*)\" doi', str(item)))
                if year and int(year) in years:
                    data['YEAR'].append(year)
                    data['TITLE'].append(fun_result(re.search('titulo-do-livro=\"(.*)\" titulo-do-livro-i', str(item))))
                    data['LANG'].append(fun_result(re.search('idioma=\"(.*)\" meio-de-divulgacao=', str(item))))
                    detalhe = livpuborg.find('detalhamento-do-livro')
                    data['EDITORA'].append(fun_result(re.search('nome-da-editora=\"(.*)\" volume', str(detalhe))))
                    authors = [fun_result(re.search('nome-completo-do-autor=\"(.*)\" nome-para-citacao', str(aut))) for
                               aut in livpuborg.find_all('autores')]
                    data['AUTHORS'].append(authors)

        return pd.DataFrame(data)


# Exemplo de uso da função com múltiplos anos
directory_path = '/caminho/dos/arquivos/'  #SETAR O CAMINHO DO ARQUIVO COM UM OU MAIS .ZIP (OS ARQUIVOS PRECISAM ESTAR EM ZIP)
years_of_interest = [2023]  # Lista dos anos de interesse
process_livros(directory_path, years_of_interest)