import pandas as pd

def join_dfs(cnpj_path,ctf_path):
    df_cnpj = pd.read_csv(cnpj_path)
    df_ctf = pd.read_csv(ctf_path)

    new_df = df_cnpj.merge(df_ctf,
                       how="left",
                       on="CNPJ")
    
    new_df.to_csv("planilha_consolidada.csv", index=False)
