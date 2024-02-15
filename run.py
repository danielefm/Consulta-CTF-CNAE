import os
import requests
import zipfile
import pandas as pd
from get_files_online import get_files_online
from transform_cnpj import transform_cnpj
from transform_ctf import transform_ctf
from join_dfs import join_dfs

# Diretório de trabalho (salvar arquivos temporários)
temp_dir = 'temp_folder'

# Diretório final (salvar arquivos que vão alimentar o BI)
final_dir = 'fonte_BI'

# Lista de URLs para download de arquivos ZIP
cnpj_url_list = [
    'http://dadosabertos.rfb.gov.br/CNPJ/Estabelecimentos0.zip',
    'http://dadosabertos.rfb.gov.br/CNPJ/Estabelecimentos1.zip',
    'http://dadosabertos.rfb.gov.br/CNPJ/Estabelecimentos2.zip',
    'http://dadosabertos.rfb.gov.br/CNPJ/Estabelecimentos3.zip',
    'http://dadosabertos.rfb.gov.br/CNPJ/Estabelecimentos4.zip',
    'http://dadosabertos.rfb.gov.br/CNPJ/Estabelecimentos5.zip',
    'http://dadosabertos.rfb.gov.br/CNPJ/Estabelecimentos6.zip',
    'http://dadosabertos.rfb.gov.br/CNPJ/Estabelecimentos7.zip',
    'http://dadosabertos.rfb.gov.br/CNPJ/Estabelecimentos8.zip',
    'http://dadosabertos.rfb.gov.br/CNPJ/Estabelecimentos9.zip'   
]

# Lista de URLs para os dados do CTF
url_base = "http://dadosabertos.ibama.gov.br/dados/CTF/APP/"
estados = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
           "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
           "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

ctf_url_list = []

for estado in estados:
    url = f"{url_base}{estado}/pessoasJuridicas.csv"
    ctf_url_list.append(url)

###### Download dos dados da Receita Federal

#get_files_online(cnpj_url_list, temp_dir)
#transform_cnpj(temp_dir, final_dir)


#get_files_online(ctf_url_list, temp_dir)
transform_ctf(temp_dir, final_dir)

#join_dfs(os.path.join(cnpj_dir, 'CNPJ_final.csv'),
#         os.path.join(ctf_dir, 'CTF_final.csv'))