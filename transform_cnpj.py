import os
import pandas as pd

def transform_cnpj(caminho_pasta, caminho_saida):
    
    # Importar cada CSV como um DataFrame e aplicar as transformações

    empresas = []  # Uma lista para armazenar todos os DataFrames após as transformações
    cnaes_empresas = []

    for arquivo in os.listdir(caminho_pasta):

        if arquivo == ".DS_Store":
            continue  # Ignorar o arquivo .DS_Store
        
        caminho_arquivo = os.path.join(caminho_pasta, arquivo)

        print(caminho_arquivo)
            
        # Importar o CSV como DataFrame
        df = pd.read_csv(caminho_arquivo,
                         encoding="windows-1251",
                         delimiter=";",
                         names=list(range(0,29)),
                         index_col=False,
                         dtype=str)
            
        # Excluir as colunas que não são necessárias
        cols = [0,1,2,4,5,11,12]
        df = df.iloc[:,cols]
            
        # Manter apenas as linhas com o valor "02" na coluna de situação da empresa
        df = df[df[5]=="02"]

        # Reformatar as colunas com o número de CNPJ
        #df['CNPJ'] = df[0].str[:2] + '.' + df[0].str[2:5] + '.' + df[0].str[5:8] + '/' + df[1] + '-' + df[2]
        df['cnpj'] = df[0].str[:2] + df[0].str[2:5] + df[0].str[5:8] + df[1] + df[2]

        df = df.rename(columns={4:'nome_fantasia',
                                11:'cnae_primario',
                                12:'cnaes_secundarios'}
                      )
        
        empresa = df[['cnpj','nome_fantasia']]

        cnae_empresa = df[['cnpj','cnae_primario','cnaes_secundarios']].astype("string")

        # NORMALIZANDO OS CNAES
        # Transformando cnaes_secundarios em listas
        cnae_empresa['cnaes_secundarios'] = cnae_empresa['cnaes_secundarios'].str.split(',')

        # Criando DataFrame com cnae primário
        df_primario = cnae_empresa[['cnpj', 'cnae_primario']].copy()
        df_primario.rename(columns={'cnae_primario': 'cnae'}, inplace=True)

        # Adicionando os cnaes secundários ao DataFrame
        df_secundario = cnae_empresa[['cnpj', 'cnaes_secundarios']].copy()
        df_secundario = df_secundario.explode('cnaes_secundarios').dropna()
        df_secundario.rename(columns={'cnaes_secundarios': 'cnae'}, inplace=True)

        # Concatenando os DataFrames
        df_final = pd.concat([df_primario, df_secundario], ignore_index=True)
        cnaes_empresas.append(df_final)
        empresas.append(empresa)

    # Consolidar os DataFrames em um único DataFrame
    cnaes_empresas_consolidado = pd.concat(cnaes_empresas, ignore_index=True)
    empresas_consolidado = pd.concat(empresas, ignore_index=True)

    # Salvar o DataFrame consolidado como um novo arquivo CSV
    cnaes_empresas_consolidado.to_csv(os.path.join(caminho_saida, 'cnae_empresas.csv'), index=False)
    empresas_consolidado.to_csv(os.path.join(caminho_saida, 'empresas.csv'), index=False)
                                      