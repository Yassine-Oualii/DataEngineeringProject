"""Quick check of ML dataset"""
import pandas as pd

df = pd.read_csv('data/ml_features_and_labels.csv')
print('Dataset shape:', df.shape)
print('\nNull values per column:')
nulls = df.isnull().sum()
print(nulls[nulls > 0].head(15))
print('\nLabel distribution:')
print(df['y'].value_counts())
print(f'\nRows with forward return data: {(~df["stock_fwd_ret_21d"].isna()).sum()}')
print(f'Rows missing forward return (last 21 days): {df["stock_fwd_ret_21d"].isna().sum()}')
print('\nSample rows:')
print(df[['Date', 'stock', 'y', 'r_1W', 'r_1M', 'vol_1M', 'VIX_t']].head(10))

