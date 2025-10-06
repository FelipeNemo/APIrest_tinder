# https://www.kaggle.com/datasets/joniarroba/noshowappointments?resource=download
import csv
import pandas as pd
CSV_PATH = 'archive/KaggleV2-May-2016.csv'

with open(CSV_PATH, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    headers = next(reader)
    print(headers)
    




# 1. Carregar o arquivo CSV para um DataFrame do Pandas
try:
    df = pd.read_csv(CSV_PATH)

    # 2. Usar o método .info() no DataFrame para ver os tipos de dados
    print("\n--- Informações do Dataset ---")
    df.info()
    df.head()

except FileNotFoundError:
    print(f"Erro: O arquivo não foi encontrado no caminho especificado: {CSV_PATH}")