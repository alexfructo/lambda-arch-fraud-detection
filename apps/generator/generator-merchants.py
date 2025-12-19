import pandas as pd

df = pd.read_csv('../../data/minio/bronze/fraudTest.csv')
json = df['merchant'].str.replace('fraud_','').drop_duplicates().copy().reset_index(drop=True)
print(json.to_json(orient='records'))