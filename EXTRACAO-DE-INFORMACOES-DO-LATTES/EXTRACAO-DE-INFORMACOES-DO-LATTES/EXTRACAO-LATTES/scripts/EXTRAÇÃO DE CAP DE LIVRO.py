#%%
# EXTRAÇÃO DOS CAPITULOS DE LIVROS
import os
import zipfile
import re
from bs4 import BeautifulSoup
import pandas as pd


def fun_result(result):
    """Função auxiliar para extrair conteúdo de expressões regulares."""
    return result.group(1) if result is not None else 'VAZIO'


# DataFrame global para acumular os dados de todos os currículos
df_all_chapters = pd.DataFrame()


def process_capitulos(directory, years):
    """Processa cada arquivo ZIP no diretório especificado, extrai e acumula dados sobre capítulos de livros publicados nos anos especificados."""
    global df_all_chapters
    df_all_chapters = pd.DataFrame()  # Reinicializa para evitar acumular dados de chamadas anteriores

    for filename in os.listdir(directory):
        if filename.endswith(".zip"):
            zip_path = os.path.join(directory, filename)
            print(f"Processando {zip_path}...")
            df_current_chapters = getcapit(zip_path, years)
            df_all_chapters = pd.concat([df_all_chapters, df_current_chapters], ignore_index=True)

    # Exporta os dados acumulados para um único arquivo CSV
    output_dir = './CAPÍTULO DE LIVROS'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    all_chapters_path = f'{output_dir}/all_chapters_{",".join(map(str, years))}.csv'
    df_all_chapters.to_csv(all_chapters_path, index=False)
    print(f'Todos os dados de capítulos foram gravados em {all_chapters_path}')


def getcapit(zip_path, years):
    """Função para extrair informações de capítulos de livros publicados ou organizados nos anos especificados."""
    with zipfile.ZipFile(zip_path, 'r') as archive:
        try:
            lattesxmldata = archive.open('curriculo.xml')
        except KeyError:
            print(f"curriculo.xml não encontrado em {zip_path}")
            return pd.DataFrame()  # Retorna um DataFrame vazio em caso de falha
        soup = BeautifulSoup(lattesxmldata, 'lxml', from_encoding='ISO-8859-1')

        # Inicializa listas para dados extraídos
        data = {
            'TITLE': [],
            'YEAR': [],
            'LANG': [],
            'EDITORA': [],
            'AUTHORS': []
        }

        livscaps = soup.find_all('livros-e-capitulos')
        capspuborg = livscaps[0].find_all('capitulos-de-livros-publicados') if livscaps else []

        for cappuborg in capspuborg[0].find_all('capitulo-de-livro-publicado') if capspuborg else []:
            dbc = cappuborg.find_all('dados-basicos-do-capitulo')
            for item in dbc:
                year = fun_result(re.search('ano=\"(.*)\" doi', str(item)))
                if year and int(year) in years:
                    data['YEAR'].append(year)
                    data['TITLE'].append(fun_result(re.search('titulo-do-capitulo-do-livro=\"(.*)\"', str(item))))
                    data['LANG'].append(fun_result(re.search('idioma=\"(.*)\"', str(item))))
                    detalhe = cappuborg.find('detalhamento-do-capitulo')
                    data['EDITORA'].append(fun_result(re.search('nome-da-editora=\"(.*)\"', str(detalhe))))
                    authors = [fun_result(re.search('nome-completo-do-autor=\"(.*)\"', str(aut))) for aut in
                               cappuborg.find_all('autores')]
                    data['AUTHORS'].append(", ".join(authors))

        return pd.DataFrame(data)


# Exemplo de uso da função com múltiplos anos
directory_path = '/caminho/dos/arquivos/'  #SETAR O CAMINHO DO ARQUIVO COM UM OU MAIS .ZIP (OS ARQUIVOS PRECISAM ESTAR EM ZIP)
years_of_interest = [2023]  # Lista dos anos de interesse
process_capitulos(directory_path, years_of_interest)