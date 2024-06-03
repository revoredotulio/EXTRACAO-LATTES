#%%
# EXTRAÇÃO OUTRAS PUBLICAÇÕES
import os
import zipfile
import re
from bs4 import BeautifulSoup
import pandas as pd


def fun_result(result):
    """Função auxiliar para extrair conteúdo de expressões regulares."""
    return result.group(1) if result is not None else 'VAZIO'


def getprodtec(zipname, input_dir, years_filter):
    """Extrai informações de produção técnica de um arquivo ZIP para os anos especificados."""
    zipfilepath = os.path.join(input_dir, zipname)
    with zipfile.ZipFile(zipfilepath, 'r') as archive:
        lattesxmldata = archive.open('curriculo.xml')
        soup = BeautifulSoup(lattesxmldata, 'lxml', from_encoding='ISO-8859-1')

        dtpt = soup.find_all('demais-tipos-de-producao-tecnica')
        all_data = []
        if len(dtpt) == 0:
            print('Demais tipos de produção não encontrada para', zipname)
            return all_data

        for dtpt_item in dtpt:
            ccdm = dtpt_item.find_all('curso-de-curta-duracao-ministrado')
            if len(ccdm) == 0:
                continue

            for curso in ccdm:
                year = fun_result(re.search('ano=\"(.*)\" doi', str(curso)))
                if year in years_filter:
                    name = fun_result(re.search('titulo=\"(.*)\" titulo-ingl', str(curso)))
                    integrantes = [
                        fun_result(re.search('nome-completo-do-autor=\"(.*)\" nome-para-citacao', str(autor))) for autor
                        in curso.find_all('autores')]
                    all_data.append({'YEAR': year, 'COURSE': name, 'INTEGRANTES': integrantes})

        return all_data


def process_zip_files(input_dir, output_dir, years_filter):
    """Processa arquivos ZIP em um diretório para extrair informações de produção técnica para os anos especificados e salva em um arquivo CSV."""
    all_data = []
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".zip"):
            print(f"Processando {filename}...")
            data = getprodtec(filename, input_dir, years_filter)
            all_data.extend(data)

    if all_data:
        df = pd.DataFrame(all_data)
        output_filename = os.path.join(output_dir, 'all_production_technical_data.csv')
        df.to_csv(output_filename, index=False)
        print(f"Todos os dados de produção técnica foram exportados para {output_filename}")
    else:
        print("Nenhum dado de produção técnica encontrado para os anos especificados.")


# Diretórios de entrada e saída
directory_path = '/caminho/dos/arquivos/'  #SETAR O CAMINHO DO ARQUIVO COM UM OU MAIS .ZIP (OS ARQUIVOS PRECISAM ESTAR EM ZIP)
output_dir = './OUTRAS PUBLICAÇÕES'  # Diretório onde o arquivo Excel será salvo
# Anos para filtrar
years_to_filter = ['2023']
process_zip_files(input_dir, output_dir, years_to_filter)