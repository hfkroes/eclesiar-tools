import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def sumarizar_categoria(df, df_name, categoria):
    sumario_categoria = df[categoria].value_counts()
    print(f"\nSumario {df_name}:\n{sumario_categoria}")

def conta_e_soma(df, categoria):
    df_resultante = df.groupby(categoria).agg(
        Transacoes=(categoria, 'size'),
        Valor=('Valor', 'sum') 
    ).reset_index()
    df_resultante = df_resultante.sort_values(by='Valor', ascending=False)
    total_transacoes = df_resultante['Transacoes'].sum()
    total_valor = df_resultante['Valor'].sum()
    total_linha = pd.DataFrame({categoria: ['Total'], 'Transacoes': [total_transacoes], 'Valor': [total_valor]})
    df_resultante = pd.concat([df_resultante, total_linha], ignore_index=True)
    df_resultante['TransacaoMedia'] = df_resultante['Valor'] / df_resultante['Transacoes']
    print(df_resultante)

    return df_resultante

# Lendo o arquivo .txt com o registro das transações
arquivo = open("abc.txt", "r")
conteudo = ""
for linha in arquivo.readlines():
    conteudo += linha
arquivo.close()

# Formatando as transações e seus subcomponentes em uma lista
temp = re.sub(r'\b(1|2|3|4|5|6|7|8|9|10|11|12|13|14|15) hours ago\b', '05-11-2024\n', conteudo)
temp = re.sub(r'\b(16|17|18|19|20|21|22|23|24) hours ago\b', '05-11-2024\n', temp)
print(temp)
temp = re.split(r'(?<=\d{2}-\d{2}-\d{4})', temp)
temp = [item.strip('\n\n\n') for item in temp]
temp = [item.replace('\n\n\n\n', '\t') for item in temp]
temp = [item.replace('\n\ncurrencies', '') for item in temp]

# Renomeando categorias de transação para o português
temp = [item.replace('Donation', 'Doação') for item in temp]
temp = [item.replace('Building construction order started', 'Construção de estrutura') for item in temp]
temp = [item.replace('New congress proposal', 'Propostas do Congresso') for item in temp]
temp = [item.replace('Invasion costs', 'Custos de invasão') for item in temp]
temp = [item.replace('Contract trade', 'Troca por contrato') for item in temp]
temp = [item.replace('Currency Exchange', 'Mercado monetário') for item in temp]
temp = [item.replace('Job wage', 'Salários') for item in temp]
temp = [item.replace('Items bought in the market', 'Itens comprados no mercado') for item in temp]
temp = [item.replace('Print money proposal result', 'Emissão de moeda') for item in temp]
temp = [item.replace('Vat Taxes', 'Imposto sobre bens') for item in temp]
temp = [item.replace('Work Taxes', 'Imposto sobre trabalho') for item in temp]
temp = [item.replace('Work taxes', 'Imposto sobre trabalho') for item in temp]
temp = [item.replace('Print money proposal', 'Custo para emissão de moeda') for item in temp]

# Criando dataframe do pandas contendo transações
transacoes = [item.split('\t') for item in temp]
transacoes = pd.DataFrame(transacoes)
print(transacoes)
print(print(transacoes.iloc[0].values))
transacoes.columns = ['Transacao', 'De', 'Para', 'Dinheiro', 'Categoria', 'Data']
transacoes[['Valor', 'Moeda']] = transacoes['Dinheiro'].str.split(' ', expand=True)
transacoes['Valor'] = transacoes['Valor'].astype(float)

# Analizando entradas
entradas = transacoes[transacoes['Para'].isin(['Pampa S/A.'])]
entradas = entradas[~entradas['Categoria'].isin(['Custos de invasão', 'Construção de estrutura', 'Propostas do Congresso', 'Custo para emissão de moeda'])]
sumarizar_categoria(entradas, "entradas", "Moeda")

doacoes = entradas[entradas['Categoria'].isin(['Doação'])]
print(doacoes)
doacoes_gold = doacoes[~doacoes['Moeda'].isin(['BRL'])]
conta_e_soma(doacoes_gold, 'De')

entradas_vat = entradas[entradas['Categoria'].isin(['Imposto sobre bens'])]
vat = conta_e_soma(entradas_vat, 'Data')

entradas_wt = entradas[entradas['Categoria'].isin(['Imposto sobre trabalho'])]
wt = conta_e_soma(entradas_wt, 'Data')

entradas_brl = entradas[entradas['Moeda'].isin(['BRL'])]
sumarizar_categoria(entradas_brl, "entradas em BRL", "Categoria")
entradas_brl_df = conta_e_soma(entradas_brl, 'Categoria')

entradas_gold = entradas[entradas['Moeda'].isin(['Gold'])]
sumarizar_categoria(entradas_gold, "entradas em Gold", "Categoria")
entradas_gold_df = conta_e_soma(entradas_gold, 'Categoria')

entradas_outras = entradas[~entradas['Moeda'].isin(['BRL', 'Gold'])]
sumarizar_categoria(entradas_outras, "entradas em outras moedas", "Categoria")
entradas_outras_df = conta_e_soma(entradas_outras, 'Categoria')

# Analizando saídas
saidas = transacoes[transacoes['De'].isin(['Pampa S/A.'])]
saidas = saidas[~saidas['Categoria'].isin(['Emissão de moeda'])]
sumarizar_categoria(saidas, "saídas", "Moeda")

saidas_brl = saidas[saidas['Moeda'].isin(['BRL'])]
sumarizar_categoria(saidas_brl, "saidas em BRL", "Categoria")
saidas_brl_df = conta_e_soma(saidas_brl, 'Categoria')

saidas_gold = saidas[saidas['Moeda'].isin(['Gold'])]
sumarizar_categoria(saidas_gold, "saídas em Gold", "Categoria")
saidas_gold_df = conta_e_soma(saidas_gold, 'Categoria')

saidas_outras = saidas[~saidas['Moeda'].isin(['BRL', 'Gold'])]
sumarizar_categoria(saidas_outras, "saídas em outras moedas", "Categoria")
saidas_outras_df = conta_e_soma(saidas_outras, 'Categoria')
