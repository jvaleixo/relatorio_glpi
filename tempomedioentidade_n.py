import pandas as pd
import matplotlib.pyplot as plt


# Caminho do CSV
arquivo = '/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/glpi_downloads/filtrado.csv'

# Lê o CSV
df = pd.read_csv(arquivo, sep=',',encoding='utf-8')

# Mostra as colunas disponíveis
print("Colunas disponíveis:", df.columns.tolist())

# Nomes das colunas (ajuste se necessário)
col_entidade = 'Atribuído - Técnico'
col_abertura = 'Data de abertura'
col_fechamento = 'Última atualização'

# Converte colunas de data
df[col_abertura] = pd.to_datetime(df[col_abertura], errors='coerce', dayfirst=True)
df[col_fechamento] = pd.to_datetime(df[col_fechamento], errors='coerce', dayfirst=True)

# Remove linhas com dados ausentes
df = df.dropna(subset=[col_abertura, col_fechamento, col_entidade])

# Nome (ou parte do nome) da pessoa que você quer analisar
pessoa = 'Rafael'  

# Filtra registros contendo o nome da pessoa (case-insensitive, ignora NaN)
df_pessoa = df[df[col_entidade].str.contains(pessoa, case=False, na=False)]

# Verifica se encontrou registros
if df_pessoa.empty:
    print(f"\n⚠️ Nenhum dado de resolução encontrado para '{pessoa}'.")
else:
    # Calcula tempo de resolução
    df_pessoa['tempo_resolucao'] = df_pessoa[col_fechamento] - df_pessoa[col_abertura]

    # Calcula a média
    media_resolucao = df_pessoa['tempo_resolucao'].mean()

    # Converte para dias
    media_resolucao_dias = media_resolucao.total_seconds() / 86400

    # Exibe o resultado
    print(f"\n📊 Média de tempo de resolução de '{pessoa}': {media_resolucao_dias:.2f} dias")



