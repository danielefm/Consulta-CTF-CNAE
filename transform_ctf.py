import os
import pandas as pd

def transform_ctf(caminho_pasta, caminho_upload):
    
    # Passo 1: Importar cada CSV como um DataFrame e aplicar as transformações

    dfs_razao_social = []  # Uma lista para armazenar todos os DataFrames após as transformações
    dfs_ctf = []

    for arquivo in os.listdir(caminho_pasta):
        caminho_arquivo = os.path.join(caminho_pasta, arquivo)
        
        print(caminho_arquivo)

        if arquivo == ".DS_Store":
            continue  # Ignorar o arquivo .DS_Store

        # Passo 1: Importar o CSV como DataFrame
        df = pd.read_csv(caminho_arquivo,
                         encoding="utf-8",
                         delimiter=";",
                         index_col=False,
                         dtype=str
                        )
            
        # Passo 2: Formatar o CNPJ
        df['CNPJ'] = df["CNPJ"].str[:2] + '.' + df["CNPJ"].str[2:5] + '.' + df["CNPJ"].str[5:8] + '/' + df["CNPJ"].str[8:12] + '-' + df["CNPJ"].str[12:]
        
        # Passo 3: Manter apenas as linhas que não tenham data de término da atividade
        df = df[df['Data de término da atividade'].isna()]

        # Passo 4:  Manter apenas as empresas que tenham situação cadastral ativa
        df = df[df["Situação cadastral"]=="Ativa"]

        # Passo 5: Criar uma coluna com a atividade do CTF consolidada
        df["CatCTF"] = df['Código da categoria'].map(str) + '-' + df['Código da atividade'].map(str)

        # Passo 6: Manter apenas as colunas de interesse
        df_razao_social = df[["CNPJ", "Razão Social"]].drop_duplicates()
        dfs_razao_social.append(df_razao_social)
        
        df_ctf = df[["CNPJ", "CatCTF"]].drop_duplicates()
        dfs_ctf.append(df_ctf)

    # Passo 7: Consolidar os DataFrames em um único DataFrame
    df_razao_social_consolidado = pd.concat(dfs_razao_social, ignore_index=True)
    df_ctf_consolidado = pd.concat(dfs_ctf,ignore_index=True)

    # Passo 8 Salvar o DataFrame consolidado como um novo arquivo CSV
    caminho_saida = os.path.join(caminho_upload, 'cnpj_razao_social.csv')  # Substitua pelo caminho e nome do arquivo desejado
    df_razao_social_consolidado.to_csv(caminho_saida, index=False)

    caminho_saida = os.path.join(caminho_upload, 'cnpj_ctf.csv')  # Substitua pelo caminho e nome do arquivo desejado
    df_ctf_consolidado.to_csv(caminho_saida, index=False)

    # Apagar todos os arquivos da pasta de trabalho
    for arquivo in os.listdir(caminho_pasta):
        os.remove(os.path.join(caminho_pasta, arquivo))