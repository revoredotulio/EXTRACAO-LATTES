#%%
# EXTRAÇÃO DAS DISCIPLINAS MINISTRADAS
import os
import zipfile
import re
from bs4 import BeautifulSoup
import pandas as pd


# Função auxiliar para extrair conteúdo de expressões regulares
def fun_result(result):
    if result is None:
        return 'VAZIO'
    else:
        return result.group(1)


# Função para processar as disciplinas ministradas
def process_disciplines(zip_path, df_ens_global):
    with zipfile.ZipFile(zip_path, 'r') as archive:
        try:
            lattesxmldata = archive.open('curriculo.xml')
            soup = BeautifulSoup(lattesxmldata, 'lxml', from_encoding='ISO-8859-1')
        except KeyError:
            print(f'curriculo.xml não encontrado em {zip_path}')
            return

        ap = soup.find_all('atuacao-profissional')
        if len(ap) == 0:
            print(f'Atuação profissional não encontrada para {zip_path}')
            return

        ls_inst = []
        ls_yini = []
        ls_yfin = []
        ls_mini = []
        ls_mfin = []
        ls_curs = []
        ls_tipo = []
        ls_disc = []
        ls_name = []

        for i in range(len(ap)):
            instit = fun_result(re.search('nome-instituicao=\"(.*)\" sequencia-atividade', str(ap[i])))
            app = ap[i].find_all('atividades-de-ensino')
            if len(app) == 0:
                print(f'Atividades de ensino não encontrada para {zip_path}')
                continue

            for j in range(len(app)):
                ens = app[j].find_all('ensino')
                if len(ens) == 0:
                    print(f'Ensino não encontrado para {zip_path}')
                    continue

                for k in range(len(ens)):
                    aten = str(ens[k])
                    ls_inst.append(instit)
                    ls_yini.append(fun_result(re.search('ano-inicio=\"(.*)\" codigo-curso', aten)))
                    ls_mini.append(fun_result(re.search('mes-inicio="(.*)" nome-curso=', aten)))
                    yfin = fun_result(re.search('ano-fim="(.*)" ano-inicio', aten))
                    ls_yfin.append(yfin if yfin != '' else 'ATUAL')
                    mfin = fun_result(re.search('mes-fim="(.*)" mes-inicio', aten))
                    ls_mfin.append(mfin if mfin != '' else 'ATUAL')
                    ls_curs.append(fun_result(re.search('nome-curso=\"(.*)\" nome-curso-i', aten)))
                    ls_tipo.append(fun_result(re.search('tipo-ensino=\"(.*)\"\>\<', aten)))
                    ensdisc = ens[k].find_all('disciplina')
                    ls_name.append(fun_result(re.search('name=\"(.*)\"\>\<', aten)))
                    ls_dis = []
                    for kk in range(len(ensdisc)):
                        dis = str(ensdisc[kk])
                        result = re.search('=\"\d\"\>(.*)\<\/disciplina', dis)
                        cc = fun_result(result)
                        ls_dis.append(cc)
                    ls_disc.append(ls_dis if ls_dis else ['VAZIO'])

        # Concatena os dados coletados ao DataFrame global
        df_temp = pd.DataFrame({
            'INSTITUTION': ls_inst,
            'YEAR_INI': ls_yini,
            'YEAR_FIN': ls_yfin,
            'MONTH_INI': ls_mini,
            'MONTH_FIN': ls_mfin,
            'COURSE': ls_curs,
            'TYPE': ls_tipo,
            'DISC': ls_disc,
            'NAME': ls_name
        })
        df_ens_global = pd.concat([df_ens_global, df_temp], ignore_index=True)
        return df_ens_global


def process_zip_files(directory):
    df_ens_global = pd.DataFrame()  # DataFrame global para armazenar os dados de todos os arquivos
    for filename in os.listdir(directory):
        if filename.endswith(".zip"):
            zip_path = os.path.join(directory, filename)
            print(f"Processando {zip_path}...")
            df_ens_global = process_disciplines(zip_path, df_ens_global)
    return df_ens_global


# Caminho para o diretório contendo os currículos em formato ZIP
directory_path = '/caminho/dos/arquivos/'  #SETAR O CAMINHO DO ARQUIVO COM UM OU MAIS .ZIP (OS ARQUIVOS PRECISAM ESTAR EM ZIP)

# Processamento dos arquivos ZIP e coleta das disciplinas ministradas
df_ens_global = process_zip_files(directory_path)

# Ordena o DataFrame global por ano de início e salva em um único arquivo CSV
output_dir = './DISCIPLINAS'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
pathfilename = f'{output_dir}/all_disciplines.csv'
df_ens_global.sort_values(['YEAR_INI'], axis=0, inplace=True)
df_ens_global.to_csv(pathfilename, index=False)
print(f'{pathfilename} gravado com {len(df_ens_global)} atividades de ensino')