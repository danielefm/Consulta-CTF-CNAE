import os
import requests
import zipfile
import pandas as pd

def get_files_online(url_list, download_dir):

    # Crie o diretório de destino se ele não existir
    os.makedirs(download_dir, exist_ok=True)
    file_counter = 0  # Inicialize um contador


    # Loop para baixar os arquivos ZIP
    for url in url_list:
        # Obtenha o nome do arquivo ZIP a partir da URL
        file_name = os.path.join(download_dir, f'file_{file_counter}_{os.path.basename(url)}')
        file_counter += 1  # Incrementa o contador para o próximo arquivo

        # Faça o download do arquivo ZIP
        response = requests.get(url, verify=False)

        if response.status_code == 200:
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f'Downloaded {file_name}')
        else:
            print(f'Failed to download {url}')

    # Diretório de destino para extrair os arquivos ZIP
    extract_dir = download_dir

    # Crie o diretório de destino para a extração
    os.makedirs(extract_dir, exist_ok=True)

    # Loop para extrair os arquivos ZIP e apagar os originais
    for file_name in os.listdir(download_dir):
        if file_name.endswith('.zip'):
            with zipfile.ZipFile(os.path.join(download_dir, file_name), 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            print(f'Extracted {file_name}')
            
            # Apague o arquivo ZIP original
            os.remove(os.path.join(download_dir, file_name))
            print(f'Deleted {file_name}')
