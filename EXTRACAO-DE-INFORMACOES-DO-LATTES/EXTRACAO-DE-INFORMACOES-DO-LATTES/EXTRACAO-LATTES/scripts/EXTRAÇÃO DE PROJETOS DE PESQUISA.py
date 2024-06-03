#%%
# EXTRAÇÃO DOS PROJETOS DE PESQUISA
import os
import zipfile
import re
from bs4 import BeautifulSoup
import pandas as pd


# Função auxiliar para extrair conteúdo de expressões regulares
def fun_result(result):
    return result.group(1) if result is not None else 'VAZIO'


# Função para processar projetos de pesquisa de currículos
def getprojpesqext(zip_path, years):
    with zipfile.ZipFile(zip_path, 'r') as archive:
        try:
            lattesxmldata = archive.open('curriculo.xml')
        except KeyError:
            print(f"curriculo.xml não encontrado em {zip_path}")
            return []
        soup = BeautifulSoup(lattesxmldata, 'lxml', from_encoding='ISO-8859-1')

        ap = soup.find_all('atuacao-profissional')
        if not ap:
            print('Atuação profissional não encontrada para', zip_path)
            return []

        all_projects = []

        for i in range(len(ap)):
            app = ap[i].find_all('atividades-de-participacao-em-projeto')
            if not app:
                continue

            for j in range(len(app)):
                ppe = app[j].find_all('projeto-de-pesquisa')
                for k in range(len(ppe)):
                    proj = str(ppe[k])
                    year_ini = fun_result(re.search('ano-inicio="(.*)" data-certificacao', proj))
                    year_fin = fun_result(re.search('ano-fim="(.*)" ano-inicio', proj))

                    # Filtra pelo ano se especificado
                    if year_ini in years or (year_fin in years or year_fin == 'ATUAL'):
                        project_data = {
                            'PROJ': fun_result(re.search('nome-do-projeto=\"(.*)\" nome-do-projeto-i', proj)),
                            'YEAR_INI': year_ini,
                            'YEAR_FIN': year_fin if year_fin else 'ATUAL',
                            'NATUREZA': fun_result(re.search('natureza=\"(.*)\" nome-coordenador', proj))
                        }
                        all_projects.append(project_data)

        return all_projects


def process_zip_files(directory, years):
    all_data = []
    for filename in os.listdir(directory):
        if filename.endswith(".zip"):
            zip_path = os.path.join(directory, filename)
            print(f"Processando {zip_path}...")
            projects_data = getprojpesqext(zip_path, years)
            all_data.extend(projects_data)

    if all_data:
        output_dir = './PROJETOS DE PESQUISA'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        df_ppe = pd.DataFrame(all_data)
        output_path = f'{output_dir}/all_projects_{"_".join(years)}.csv'
        df_ppe.to_csv(output_path, index=False)
        print(f'{output_path} gravado com {len(df_ppe)} projetos')


# Caminho para o diretório contendo os currículos em formato ZIP
directory_path = '/caminho/dos/arquivos/'  #SETAR O CAMINHO DO ARQUIVO COM UM OU MAIS .ZIP (OS ARQUIVOS PRECISAM ESTAR EM ZIP)
years_to_filter = ['2023']
process_zip_files(directory_path, years_to_filter)