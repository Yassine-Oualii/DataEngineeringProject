import pandas as pd

df_before = pd.read_csv('data/integrated_prepared_data.csv')
df_after = pd.read_csv('data/integrated_scaled_data.csv')
log = pd.read_csv('data/scaling_log.csv')

print("SCALING VERIFICATION:")
print("=" * 70)
print(f"\nBefore scaling - Sample values:")
print(f"Close: mean={df_before['Close'].mean():.2f}, std={df_before['Close'].std():.2f}")
print(f"Volume: mean={df_before['Volume'].mean():.0f}, std={df_before['Volume'].std():.0f}")

print(f"\nAfter scaling - Sample values:")
print(f"Close: mean={df_after['Close'].mean():.4f}, std={df_after['Close'].std():.4f}")
print(f"Volume: mean={df_after['Volume'].mean():.4f}, std={df_after['Volume'].std():.4f}")

print(f"\nMethods used:")
print(log['method'].value_counts().to_string())

