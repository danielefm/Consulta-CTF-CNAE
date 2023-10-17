import os
import pandas as pd

def TransformCTF(caminho_pasta):
    
    # Passo 1: Importar cada CSV como um DataFrame e aplicar as transformações

    dfs = []  # Uma lista para armazenar todos os DataFrames após as transformações

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

        dfs.append(df)

    # Passo 6: Consolidar os DataFrames em um único DataFrame
    df_consolidado = pd.concat(dfs, ignore_index=True)

    # Salvar o DataFrame consolidado como um novo arquivo CSV
    caminho_saida = os.path.join(caminho_pasta, 'CTF_final.csv')  # Substitua pelo caminho e nome do arquivo desejado
    df_consolidado.to_csv(caminho_saida, index=False)