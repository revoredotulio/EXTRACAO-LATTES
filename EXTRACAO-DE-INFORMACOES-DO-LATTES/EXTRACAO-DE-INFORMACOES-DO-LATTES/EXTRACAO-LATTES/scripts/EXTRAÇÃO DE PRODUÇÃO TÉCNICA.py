#%%
# EXTRAÇÃO DA PRODUÇÃO TÉCNICA
import os
import zipfile
import re
from bs4 import BeautifulSoup
import pandas as pd


def fun_result(result):
    """Função auxiliar para extrair conteúdo de expressões regulares."""
    return result.group(1) if result is not None else 'VAZIO'


# Função modificada para aceitar anos de extração como parâmetro e um DataFrame global
def process_dados_gerais(directory, anos):
    global df_fullname_global
    df_fullname_global = pd.DataFrame()  # DataFrame global para acumular os dados de todos os currículos

    for filename in os.listdir(directory):
        if filename.endswith(".zip"):
            zip_path = os.path.join(directory, filename)
            print(f"Processando {zip_path}...")
            df_fullname_individual = getnomecompleto(zip_path, anos)
            if not df_fullname_individual.empty:
                df_fullname_global = pd.concat([df_fullname_global, df_fullname_individual], ignore_index=True)
            print(f"Concluído o processamento de {zip_path}.")

    # Exporta os dados acumulados para um único arquivo CSV
    output_dir = './PRODUÇÃO TÉCNICA'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    all_dados_path = f'{output_dir}/all_dados_gerais.csv'
    df_fullname_global.to_csv(all_dados_path, index=False)
    print(f'Todos os dados de dados gerais foram gravados em {all_dados_path}')


def getnomecompleto(zip_path, anos):
    """Função modificada para extrair dados gerais dos currículos Lattes, considerando apenas os anos especificados."""
    with zipfile.ZipFile(zip_path, 'r') as archive:
        try:
            lattesxmldata = archive.open('curriculo.xml')
        except KeyError:
            print(f"curriculo.xml não encontrado em {zip_path}")
            return pd.DataFrame()  # Retorna um DataFrame vazio em caso de falha
        soup = BeautifulSoup(lattesxmldata, 'lxml', from_encoding='ISO-8859-1')

        cv = soup.find_all('curriculo-vitae')
        if len(cv) == 0:
            print(f'curriculo vitae não encontrado para {zip_path}')
            return

        # Inicialização de listas para armazenamento de dados
        ls_name_full, ls_name_last, ls_name_id, ls_city, ls_state = [], [], [], [], []
        ls_citado, ls_orcid, ls_abstrac, ls_update, ls_address_enterp = [], [], [], [], []

        # Definindo dados a partir do currículo vitae
        for i in range(len(cv)):
            # Extração de dados gerais
            ...

        # Criação do DataFrame e salvamento em arquivo CSV
        return pd.DataFrame({
            'ID': [],
            'FULL_NAME': [],
            'LAST_NAME': [],
            'CITADO': [],
            'CITY': [],
            'STATE': [],
            'RESUME': [],
            'UPDATE': [],
            'ADDRESS_ENTERP': [],
            'ORCID': []
        })


# Exemplo de uso da função com anos especificados
directory_path = '/caminho/dos/arquivos/'  #SETAR O CAMINHO DO ARQUIVO COM UM OU MAIS .ZIP (OS ARQUIVOS PRECISAM ESTAR EM ZIP)
anos_de_interesse = [2023]  # Anos que deseja extrair informações
process_dados_gerais(directory_path, anos_de_interesse)