import pandas as pd


csv_servidores_path = "dados/ServidoresMG_0824.csv"
ser_df = pd.read_csv(csv_servidores_path, encoding="ISO-8859-1",sep=";", low_memory=False)


# Dropando colunas que considero irrelevantes para esta análise e renomeando restantes
ser_df1 = ser_df.drop(ser_df.columns[[0]+[2]+[4]+list(range(10,37))], axis=1)

# Alterando nomes de colunas para facilitar chamadas 
colunas_df1 = list(ser_df1.columns)
renomear_para = ['Nome do Servidor','Ocupação', 'Complemento Ocupação', 'Órgão','Unidade','Carga Horária','Remuneração']
mudancas_colunas = dict(zip(colunas_df1,renomear_para))
ser_df1.rename(columns=mudancas_colunas,inplace=True)


# Alterando escrita de algumas colunas para permitir calculos numéricos
ser_df1['Remuneração'] = ser_df1['Remuneração'].str.replace(',','.',regex=False)
ser_df1['Remuneração'] = pd.to_numeric(ser_df1['Remuneração']).astype(float)
ser_df1['Carga Horária'] = ser_df1['Carga Horária'].str.replace(',','.',regex=False)
ser_df1['Carga Horária'] = pd.to_numeric(ser_df1['Carga Horária']).astype(float)

'''
Essa parte do código executei localmente, resulta no arquivo csv servidores_correlacionados.csv (correlaciona primeiro nome do servidor com um sexo provavel)
Tempo de execução local de aproximadamente 2 horas em um Intel Core I7 com 16gb de ram.

# Criando correlação de sexo de acordo com nome. Base de nomes e sexos retirado de trabalho realizado pelo Álvaro Justen (https://github.com/turicas)
csv_nomes_path = 'nomes.csv'
df_ibge = pd.read_csv(csv_nomes_path, sep=',')

ser_df1['Sexo provavel do servidor'] = None
ser_df1['Primeiro Nome do Servidor'] = ser_df1['Nome do Servidor'].apply(lambda nome: nome.split()[0])

for index_ser, row_ser in ser_df1.iterrows():
    nome_servidor = row_ser['Primeiro Nome do Servidor'].lower()  # Convertendo para minúsculas para consistência
    nome_correspondente = df_ibge[df_ibge['group_name'].str.lower() == nome_servidor]
    
    if not nome_correspondente.empty:
        ser_df1.at[index_ser, 'Sexo provavel do servidor'] = nome_correspondente.iloc[0]['classification']


ser_df1.to_csv('servidores_correlacionados.csv', index=False)

'''

csv_servidores_correlacionados_path = "dados/servidores_correlacionados.csv"
df_correlacionado = pd.read_csv(csv_servidores_correlacionados_path, encoding="utf-8",sep=",", low_memory=False)

# Aqui apago alguns registros (cerca de 15% que não tiveram correlação de sexo seguindo o metodo utilizado acima. Esse método de correlação nome/sexo precisa ser aprimorado posteriormente)

df_correlacionado = df_correlacionado[df_correlacionado['Sexo provavel do servidor'].notna()]