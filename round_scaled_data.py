"""
Round scaled data to reasonable precision for readability
"""
import pandas as pd
import numpy as np

print("=" * 70)
print("ROUNDING SCALED DATA TO REASONABLE PRECISION")
print("=" * 70)

# Load scaled data
print("\n1. Loading scaled data...")
df = pd.read_csv('data/integrated_scaled_data.csv')
print(f"   Loaded {len(df):,} rows, {len(df.columns)} columns")

# Show sample before rounding
print("\n2. Sample BEFORE rounding:")
sample_cols = ['Close', 'Volume', 'CPI', 'VIX']
for col in sample_cols:
    if col in df.columns:
        print(f"   {col}: {df[col].iloc[0]:.10f}")

# Round numeric columns to 6 decimal places (reasonable precision)
print("\n3. Rounding numeric columns to 6 decimal places...")
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
# Exclude Date if it's numeric
if 'Date' in numeric_cols:
    numeric_cols.remove('Date')

df_rounded = df.copy()
for col in numeric_cols:
    df_rounded[col] = df_rounded[col].round(6)

# Show sample after rounding
print("\n4. Sample AFTER rounding:")
for col in sample_cols:
    if col in df.columns:
        print(f"   {col}: {df_rounded[col].iloc[0]:.6f}")

# Save rounded data
print("\n5. Saving rounded data...")
output_file = 'data/integrated_scaled_data.csv'
df_rounded.to_csv(output_file, index=False, float_format='%.6f')
print(f"   OK Saved to: {output_file}")

print("\n" + "=" * 70)
print("EXPLANATION")
print("=" * 70)
print("""
Why negative numbers?
  - StandardScaler transforms data to mean=0, std=1
  - Values below the mean become negative
  - This is NORMAL and EXPECTED for scaled data
  - Example: If mean Close price was 115, then Close=50 becomes negative

Why long decimals?
  - Scaling can produce very precise decimal values
  - Now rounded to 6 decimal places for readability
  - Still maintains precision for machine learning

About the values:
  - Values typically range from -3 to +3 (within 3 standard deviations)
  - Values near 0 represent values near the original mean
  - Negative = below original mean, Positive = above original mean
""")

print("\n" + "=" * 70)
print("ROUNDING COMPLETE")
print("=" * 70)

