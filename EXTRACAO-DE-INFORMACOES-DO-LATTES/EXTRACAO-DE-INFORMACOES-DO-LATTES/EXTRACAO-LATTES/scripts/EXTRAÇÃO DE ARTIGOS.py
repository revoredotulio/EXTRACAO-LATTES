#%%
# EXTRAÇÃO DOS ARTIGOS PUBLICADOS

import os
import zipfile
import re
from bs4 import BeautifulSoup
import pandas as pd


def fun_result(result):
    """Função auxiliar para extrair conteúdo de expressões regulares."""
    return result.group(1) if result is not None else 'VAZIO'


def getperiod(zip_path, years):
    with zipfile.ZipFile(zip_path, 'r') as archive:
        try:
            with archive.open('curriculo.xml', 'r') as file:
                content = file.read().decode('ISO-8859-1')
        except KeyError:
            print(f"curriculo.xml não encontrado em {zip_path}")
            return pd.DataFrame()  # Retorna um DataFrame vazio em caso de falha

        soup = BeautifulSoup(content, 'lxml')  # Use 'lxml' diretamente para XML parsing

        dg = soup.find_all('dados-gerais')
        if not dg:
            print(f'Dados gerais não encontrados para {zip_path}')
            return pd.DataFrame()

        fullname = fun_result(re.search('nome-completo=\"(.*)\" nome-em-citacoes', str(dg[0])))

        pb = soup.find_all('producao-bibliografica')
        if not pb:
            print(f'Produções bibliográficas não encontradas para {zip_path}')
            return pd.DataFrame()

        artspubs = pb[0].find_all('artigos-publicados')
        if not artspubs:
            print(f'Artigos publicados não encontrados para {zip_path}')
            return pd.DataFrame()

        data = {
            'TITLE': [],
            'YEAR': [],
            'DOI': [],
            'LANG': [],
            'JOURNAL': [],
            'ISSN': [],
            'AUTHOR': [],
            'ORDER': [],
            'ORDER_OK': []
        }

        for artpub in artspubs[0].find_all('artigo-publicado'):
            dba = artpub.find_all('dados-basicos-do-artigo')
            paperdb = str(dba[0])
            year = fun_result(re.search('ano-do-artigo=\"(.*)\" doi', paperdb))
            if year and year.isdigit() and int(year) in years:
                data['TITLE'].append(fun_result(re.search('titulo-do-artigo=\"(.*)\" titulo-do-artigo-i', paperdb)))
                data['YEAR'].append(year)
                data['DOI'].append(fun_result(re.search('doi=\"(.*)\" flag-divulgacao-c', paperdb)))
                data['LANG'].append(fun_result(re.search('idioma=\"(.*)\" meio-de-divulgacao=', paperdb)))

                dda = artpub.find_all('detalhamento-do-artigo')
                paperdt = str(dda[0])
                data['JOURNAL'].append(fun_result(re.search('titulo-do-periodico-ou-revista=\"(.*)\" volume', paperdt)))

                issn = fun_result(re.search('issn=\"(.*)\" local-de-public', paperdt))
                data['ISSN'].append(issn[:4] + '-' + issn[4:] if issn != 'VAZIO' else 'VAZIO')

                aut = artpub.find_all('autores')
                authors = [fun_result(re.search('nome-completo-do-autor=\"(.*)\" nome-para-citacao', str(a))) for a in
                           aut]
                authororder = [fun_result(re.search('ordem-de-autoria=\"(.*)\"', str(a))) for a in aut]
                order_ok = [order for name, order in zip(authors, authororder) if name == fullname]
                data['AUTHOR'].append(authors)
                data['ORDER'].append(authororder)
                data['ORDER_OK'].append(order_ok)

        return pd.DataFrame(data)


def process_zip_files(directory, years):
    global df_all_papers
    df_all_papers = pd.DataFrame()  # Resetando o DataFrame global para cada chamada

    for filename in os.listdir(directory):
        if filename.endswith(".zip"):
            zip_path = os.path.join(directory, filename)
            df_current = getperiod(zip_path, years)
            df_all_papers = pd.concat([df_all_papers, df_current], ignore_index=True)

    output_dir = './ARTIGOS'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    all_periods_path = f'{output_dir}/all_periods_{",".join(map(str, years))}.csv'
    df_all_papers.to_csv(all_periods_path, index=False)
    print(f'Dados de todos os currículos foram gravados em {all_periods_path}')


# LEITURA DOS ARQUIVOS
directory_path = '/caminho/dos/arquivos/'  #SETAR O CAMINHO DO ARQUIVO COM UM OU MAIS .ZIP (OS ARQUIVOS PRECISAM ESTAR EM ZIP)
years_of_interest = [2019, 2020, 2021, 2022, 2023, 2024]  # SEPARAR OS ANOS POR VÍRGULA, SEM LIMITES DE ANO
process_zip_files(directory_path, years_of_interest)

