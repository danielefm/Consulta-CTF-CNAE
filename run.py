import os
import requests
import zipfile
import pandas as pd
from GetFilesOnline import GetFilesOnline
from TransformCNPJ import TransformCNPJ
from TransformCTF import TransformCTF
from JoinDFs import Join_DFs

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

# Diretório de destino para salvar os arquivos ZIP
cnpj_dir = 'Dados CNPJ'


# Lista de URLs para os dados do CTF
url_base = "http://dadosabertos.ibama.gov.br/dados/CTF/APP/"
estados = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
           "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
           "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

ctf_url_list = []

for estado in estados:
    url = f"{url_base}{estado}/pessoasJuridicas.csv"
    ctf_url_list.append(url)

ctf_dir = 'Dados CTF IBAMA'

###### Início do programa de fato

GetFilesOnline(cnpj_url_list,cnpj_dir)
GetFilesOnline(ctf_url_list, ctf_dir)

TransformCNPJ(cnpj_dir)
TransformCTF(ctf_dir)

Join_DFs(os.path.join(cnpj_dir, 'CNPJ_final.csv'),
         os.path.join(ctf_dir, 'CTF_final.csv'))