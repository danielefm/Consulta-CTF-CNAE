import os
import pandas as pd

def TransformCNPJ(caminho_pasta):
    
    # Passo 0: Importar cada CSV como um DataFrame e aplicar as transformações

    dfs = []  # Uma lista para armazenar todos os DataFrames após as transformações

    for arquivo in os.listdir(caminho_pasta):

        if arquivo == ".DS_Store":
            continue  # Ignorar o arquivo .DS_Store
        
        if arquivo == "CNPJ_final.csv":
            continue  # Ignorar o arquivo
        
        caminho_arquivo = os.path.join(caminho_pasta, arquivo)

        print(caminho_arquivo)
            
        # Passo 1: Importar o CSV como DataFrame
        df = pd.read_csv(caminho_arquivo,
                         encoding="windows-1251",
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
        colunas = ['CNPJ'] + [col for col in df.columns if col not in ['CNPJ', 0, 1, 2, 5]]
        df = df[colunas]

        # Passo 5: trocar as vírgulas por hífens no CNAE secundário
        df[12] = df[12].fillna('')
        df[12] = df[12].str.replace(',','-')

        # Passo 6: Consolidar CNAES principal e secundários em uma única coluna
        df['CNAE'] = df[11] + '-' + df[12]
        df = df.drop([11,12], axis=1)
        df = df.rename(columns={4:'Nome Fantasia'})

        print(df.head())

        dfs.append(df)

    # Passo 4: Consolidar os DataFrames em um único DataFrame
    df_consolidado = pd.concat(dfs, ignore_index=True)

    # Salvar o DataFrame consolidado como um novo arquivo CSV
    caminho_saida = os.path.join(caminho_pasta, 'CNPJ_final.csv')  # Substitua pelo caminho e nome do arquivo desejado
    df_consolidado.to_csv(caminho_saida, index=False)
