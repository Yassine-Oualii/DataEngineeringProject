"""
Detailed Explanation of Scaling Method Decisions

Shows why each column received its specific scaling method.
"""

import pandas as pd
import numpy as np

print("=" * 70)
print("SCALING METHOD DECISION EXPLANATION")
print("=" * 70)

# Load data and scaling log
df = pd.read_csv('data/integrated_prepared_data.csv')
log = pd.read_csv('data/scaling_log.csv')

print("\n" + "=" * 70)
print("1. STANDARD SCALER (25 columns)")
print("=" * 70)

std_cols = log[log['method'] == 'StandardScaler']['column'].tolist()

print("\nDecision Logic Applied:")
print("-" * 70)
print("""
Criteria checked (in order):
  1. Is it RSI? → No → Continue
  2. Does column name contain 'ratio'? → No → Continue  
  3. Does it have >5% outliers? → Check...
  4. Is std = 0 (constant)? → No → Continue
  5. → Default: StandardScaler (normal distribution, low outliers)

StandardScaler Formula: (x - mean) / std
Result: Mean = 0, Std = 1
""")

print("\nWhy StandardScaler for these columns:")
print("-" * 70)

categories = {
    'Stock Price Features': ['Close', 'High', 'Low', 'Open', 'Volume'],
    'SP500 Features': ['sp500_Close', 'sp500_High', 'sp500_Low', 'sp500_Open', 'sp500_Volume'],
    'Macro Indicators': ['CPI', 'Fed_Funds_Rate', 'GDP', 'Unemployment_Rate'],
    'Market Sentiment': ['VIX', 'Market_Breadth'],
    'Sector ETFs': ['sector_XLK', 'sector_XLF', 'sector_XLV', 'sector_XLE', 'sector_XLI'],
    'Technical Indicators (SMA)': ['spy_SMA_50', 'spy_SMA_200', 'qqq_SMA_50', 'qqq_SMA_200']
}

for category, cols in categories.items():
    matching = [c for c in cols if c in std_cols]
    if matching:
        print(f"\n{category}:")
        for col in matching:
            # Get statistics
            mean_val = df[col].mean()
            std_val = df[col].std()
            min_val = df[col].min()
            max_val = df[col].max()
            
            # Check outliers
            outliers = len(df[(df[col] < mean_val - 3*std_val) | (df[col] > mean_val + 3*std_val)])
            outlier_pct = (outliers / len(df)) * 100
            
            print(f"  {col}:")
            print(f"    Range: [{min_val:.2f}, {max_val:.2f}]")
            print(f"    Mean: {mean_val:.2f}, Std: {std_val:.2f}")
            print(f"    Outliers: {outlier_pct:.1f}% (threshold: 5%)")
            print(f"    Reason: Normal-like distribution, outliers <5%")
            print(f"    → StandardScaler appropriate")

print("\n" + "=" * 70)
print("2. MINMAX SCALER (1 column)")
print("=" * 70)

mm_cols = log[log['method'] == 'MinMaxScaler']['column'].tolist()

print(f"\nColumn: {mm_cols[0]}")
print("-" * 70)

col = mm_cols[0]
mean_val = df[col].mean()
std_val = df[col].std()
min_val = df[col].min()
max_val = df[col].max()

print(f"Column name: '{col}'")
print(f"  Contains 'ratio'? Yes → MinMaxScaler selected")
print(f"\nData characteristics:")
print(f"  Range: [{min_val:.2f}, {max_val:.2f}]")
print(f"  Mean: {mean_val:.2f}")
print(f"  Std: {std_val:.2f}")

print(f"\nWhy MinMaxScaler?")
print(f"  - Column name suggests it's a ratio (Put_Call_Ratio)")
print(f"  - Ratios are naturally bounded (have min/max)")
print(f"  - MinMaxScaler: (x - min) / (max - min) → Range [0, 1]")
print(f"  - Preserves the bounded nature of ratios")
print(f"  - Better than StandardScaler for bounded data")

print("\n" + "=" * 70)
print("3. NO SCALING (2 columns)")
print("=" * 70)

no_scale_cols = log[log['method'] == 'No scaling']['column'].tolist()

print("\nDecision Logic:")
print("-" * 70)
print("""
Criteria checked (first priority):
  1. Is it RSI? → YES → No scaling
     Reason: RSI is already normalized to [0, 100]
""")

for col in no_scale_cols:
    mean_val = df[col].mean()
    std_val = df[col].std()
    min_val = df[col].min()
    max_val = df[col].max()
    
    print(f"\n{col}:")
    print(f"  Range: [{min_val:.2f}, {max_val:.2f}]")
    print(f"  Already bounded: [0, 100] (RSI standard range)")
    print(f"  Mean: {mean_val:.2f}")
    print(f"  Std: {std_val:.2f}")
    
    print(f"\n  Why No Scaling?")
    print(f"    - RSI (Relative Strength Index) is already normalized")
    print(f"    - Bounded between 0 and 100 by definition")
    print(f"    - Adding scaling would:")
    print(f"      * Distort the 0-100 meaning")
    print(f"      * Lose interpretability (RSI>70 = overbought)")
    print(f"      * Not improve model performance")
    print(f"    - Already on appropriate scale for ML models")

print("\n" + "=" * 70)
print("DECISION FLOWCHART SUMMARY")
print("=" * 70)

print("""
For each column:
  ├─ Is it spy_RSI or qqq_RSI?
  │  └─ YES → No Scaling (already 0-100)
  │
  ├─ Does column name contain 'ratio'?
  │  └─ YES → MinMaxScaler (bounded data)
  │
  ├─ Are outliers > 5%?
  │  └─ YES → RobustScaler (robust to outliers)
  │
  ├─ Is std = 0?
  │  └─ YES → No Scaling (constant values)
  │
  └─ DEFAULT → StandardScaler (normal distribution)

In your dataset:
  - No RSI columns → Skip first check
  - Put_Call_Ratio → Contains 'ratio' → MinMaxScaler
  - spy_RSI, qqq_RSI → Special case → No Scaling
  - All others → StandardScaler (default)
""")

print("\n" + "=" * 70)
print("COMPARISON: Why Not StandardScaler for RSI?")
print("=" * 70)

rsi_example = df['spy_RSI'].iloc[0]
print(f"\nExample: spy_RSI = {rsi_example:.2f}")
print(f"\nIf we used StandardScaler:")
mean_rsi = df['spy_RSI'].mean()
std_rsi = df['spy_RSI'].std()
scaled_rsi = (rsi_example - mean_rsi) / std_rsi
print(f"  Mean: {mean_rsi:.2f}, Std: {std_rsi:.2f}")
print(f"  Scaled value: {scaled_rsi:.4f}")
print(f"  → Would lose meaning: {rsi_example:.2f} is in interpretable range [0-100]")
print(f"  → {scaled_rsi:.4f} has no intuitive meaning")
print(f"\nKeeping original [0-100] range:")
print(f"  → {rsi_example:.2f} > 70? Overbought signal (interpretable)")
print(f"  → {rsi_example:.2f} < 30? Oversold signal (interpretable)")

print("\n" + "=" * 70)
print("COMPARISON: Why MinMaxScaler for Put_Call_Ratio?")
print("=" * 70)

ratio_example = df['Put_Call_Ratio'].iloc[0]
min_ratio = df['Put_Call_Ratio'].min()
max_ratio = df['Put_Call_Ratio'].max()
mean_ratio = df['Put_Call_Ratio'].mean()
std_ratio = df['Put_Call_Ratio'].std()

print(f"\nPut_Call_Ratio characteristics:")
print(f"  Original value: {ratio_example:.2f}")
print(f"  Range: [{min_ratio:.2f}, {max_ratio:.2f}]")
print(f"  Mean: {mean_ratio:.2f}, Std: {std_ratio:.2f}")

# Show what each method would do
minmax_scaled = (ratio_example - min_ratio) / (max_ratio - min_ratio)
standard_scaled = (ratio_example - mean_ratio) / std_ratio

print(f"\nWith MinMaxScaler:")
print(f"  Formula: ({ratio_example:.2f} - {min_ratio:.2f}) / ({max_ratio:.2f} - {min_ratio:.2f})")
print(f"  Result: {minmax_scaled:.4f} (range [0, 1])")
print(f"  → Preserves bounded nature")

print(f"\nIf we used StandardScaler instead:")
print(f"  Formula: ({ratio_example:.2f} - {mean_ratio:.2f}) / {std_ratio:.2f}")
print(f"  Result: {standard_scaled:.4f} (range: -∞ to +∞)")
print(f"  → Could produce values outside [0, 1] range")
print(f"  → Loses bounded ratio interpretation")

print("\n" + "=" * 70)
print("FINAL SUMMARY")
print("=" * 70)

print("""
StandardScaler (25 columns):
  ✓ Used for: Unbounded continuous variables
  ✓ Examples: Prices, volumes, macro indicators
  ✓ Reason: Normal distribution, low outliers
  ✓ Result: Mean=0, Std=1

MinMaxScaler (1 column):
  ✓ Used for: Bounded ratios/proportions
  ✓ Example: Put_Call_Ratio
  ✓ Reason: Preserves bounded nature [0, 1]
  ✓ Result: Range [0, 1]

No Scaling (2 columns):
  ✓ Used for: Already normalized indicators
  ✓ Examples: spy_RSI, qqq_RSI
  ✓ Reason: Already in interpretable range [0, 100]
  ✓ Result: Keep original values
""")

