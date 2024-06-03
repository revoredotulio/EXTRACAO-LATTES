#%%
# EXTRAÇÃO DAS ORIENTAÇÕES
import os
import zipfile
import re
from bs4 import BeautifulSoup
import pandas as pd


def fun_result(result):
    """Função auxiliar para extrair conteúdo de expressões regulares."""
    return result.group(1) if result is not None else 'VAZIO'


def getorient(zipname, years, input_dir, output_dir):
    """Extrai informações de orientações de pesquisador de um arquivo ZIP e salva em um CSV no diretório especificado."""
    zipfilepath = os.path.join(input_dir, zipname)
    with zipfile.ZipFile(zipfilepath, 'r') as archive:
        lattesxmldata = archive.open('curriculo.xml')
        soup = BeautifulSoup(lattesxmldata, 'lxml', from_encoding='ISO-8859-1')

        op = soup.find_all('outra-producao')
        if len(op) == 0:
            print('Outras producoes nao encontradas para', zipname)
            return

        all_orientations = []

        for orientation_type in ['orientacoes-concluidas-para-mestrado', 'orientacoes-concluidas-para-doutorado',
                                 'outras-orientacoes-concluidas']:
            orientations = op[0].find_all(orientation_type)

            if len(orientations) == 0:
                print(f'{orientation_type.replace("-", " ").capitalize()} nao encontradas para', zipname)
                continue

            for orientation in orientations:
                basic_data = orientation.find_all(f'dados-basicos-de-{orientation_type}')
                detail = orientation.find_all(f'detalhamento-de-{orientation_type}')

                for bd, dt in zip(basic_data, detail):
                    bd_str, dt_str = str(bd), str(dt)
                    year = fun_result(re.search('ano=\"(.*)\" doi', bd_str))
                    if year in years:
                        nature = fun_result(re.search('natureza=\"(.*)\" pais', bd_str))
                        institution = fun_result(re.search('nome-da-instituicao=\"(.*)\" nome-do-curso=', dt_str))
                        course = fun_result(re.search('nome-do-curso=\"(.*)\" nome-do-curso-ingles', dt_str))
                        student = fun_result(re.search('nome-do-orientado=\"(.*)\"', dt_str))
                        orientation_type_found = fun_result(
                            re.search('tipo-de-orientacao(?:-concluida)?=\"(.*)\">', dt_str))
                        sponsor = fun_result(re.search('flag-bolsa=\"(.*)\" nome-da-agencia', dt_str))
                        all_orientations.append(
                            [year, nature, institution, course, student, orientation_type_found, sponsor])

        df = pd.DataFrame(all_orientations,
                          columns=['YEAR', 'NATURE', 'INSTITUTION', 'COURSE', 'STUDENT', 'TYPE', 'SPONSOR'])
        if not df.empty:
            pathfilename = f'{output_dir}/{zipname[:-4]}_orientations.csv'
            df.to_csv(pathfilename, index=False)
            print(f'Orientações gravadas em {pathfilename}')
        else:
            print(f'Nenhuma orientação encontrada para {zipname} nos anos especificados.')


def process_zip_files(input_dir, years):
    """Processa arquivos ZIP em um diretório para extrair orientações do pesquisador para os anos especificados e salva em um diretório de saída."""
    output_dir = './ORIENTAÇÕES'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".zip"):
            print(f"Processando {filename}...")
            getorient(filename, years, input_dir, output_dir)


# Caminho para o diretório contendo os currículos em formato ZIP
directory_path = '/caminho/dos/arquivos/'  #SETAR O CAMINHO DO ARQUIVO COM UM OU MAIS .ZIP (OS ARQUIVOS PRECISAM ESTAR EM ZIP)
years_to_process = ['2023']  # Anos que deseja filtrar
process_zip_files(directory_path, years_to_process)