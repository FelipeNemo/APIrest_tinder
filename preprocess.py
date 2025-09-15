import pandas as pd

# Lendo o CSV
df = pd.read_csv('Tinder_Data_v3_Clean_Edition.csv')

# Salvando em JSON
df.to_json('json.json', orient='records', lines=True)
