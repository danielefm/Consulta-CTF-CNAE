import os
import pandas as pd

def transform_cnpj(caminho_pasta, caminho_upload):
    
    # Passo 0: Importar cada CSV como um DataFrame e aplicar as transformações

    dfs_nomes = []  # Listas para armazenar os dataframes após as transformmações
    dfs_cnaes = []

    for arquivo in os.listdir(caminho_pasta):

        if arquivo == ".DS_Store":
            continue  # Ignorar o arquivo .DS_Store
        
        caminho_arquivo = os.path.join(caminho_pasta, arquivo)

        print(caminho_arquivo)
            
        # Passo 1: Importar o CSV como DataFrame
        df = pd.read_csv(caminho_arquivo,
                         encoding="windows-1252",
                         delimiter=";",
                         names=list(range(0,29)),
                         index_col=False,
                         dtype=str)
            
        # Passo 2: Excluir as colunas que não são necessárias
        cols = [0,1,2,4,5,11,12]
        df = df.iloc[:,cols]
            
        # Passo 3: Manter apenas as linhas com o valor "02" na coluna de situação da empresa
        df = df[df[5]=="02"]

        # Passo 4: Reformatar as colunas com o número de CNPJ
        df['CNPJ'] = df[0].str[:2] + '.' + df[0].str[2:5] + '.' + df[0].str[5:8] + '/' + df[1] + '-' + df[2]
        #df['CNPJ'] = df[0].str[:2] + df[0].str[2:5] + df[0].str[5:8] + df[1] + df[2]

        colunas = ['CNPJ'] + [col for col in df.columns if col not in ['CNPJ', 0, 1, 2, 5]]
        df = df[colunas]

        # Passo 5: trocar as vírgulas por hífens no CNAE secundário
        df[12] = df[12].fillna('')

        # Passo 6: Consolidar CNAES principal e secundários em uma única coluna
        df['CNAE'] = df[11] + ',' + df[12]
        df = df.drop([11,12], axis=1)
        
        # Adicionar ao dataframe CNPJ e Nome Fantasia
        df = df.rename(columns={4:'Nome Fantasia'})
        dfs_nomes.append(df[["CNPJ", "Nome Fantasia"]])

        # Normalizar os CNAES
        df = df.drop(columns="Nome Fantasia")
        df["CNAE"] = df["CNAE"].str.split(",")
        df = df.explode("CNAE").reset_index(drop=True)
        df = df[df.CNAE != ""].reset_index(drop=True)

        dfs_cnaes.append(df)

    # Consolidar os DataFrames em um único DataFrame
    df_nomes_consolidado = pd.concat(dfs_nomes, ignore_index=True)
    df_cnaes_consolidado = pd.concat(dfs_cnaes, ignore_index=True)

    # Salvar o DataFrame consolidado como um novo arquivo CSV
    caminho_saida = os.path.join(caminho_upload, 'cnpj_nome_fantasia.csv')
    df_nomes_consolidado.to_csv(caminho_saida, index=False)

    caminho_saida = os.path.join(caminho_upload, 'cnpj_cnaes.csv')
    df_cnaes_consolidado.to_csv(caminho_saida, index=False)

    # Apagar todos os arquivos da pasta de trabalho
    for arquivo in os.listdir(caminho_pasta):
        os.remove(os.path.join(caminho_pasta, arquivo))
