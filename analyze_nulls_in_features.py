"""
Analyze and explain null values in the ML features and labels dataset
"""

import pandas as pd
import numpy as np

print("=" * 70)
print("NULL VALUE ANALYSIS - ML FEATURES AND LABELS")
print("=" * 70)

# Load dataset
df = pd.read_csv('data/ml_features_and_labels.csv')
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(['stock', 'Date']).reset_index(drop=True)

print(f"\nDataset: {len(df):,} rows")
print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
print(f"Stocks: {df['stock'].unique()}")

# Get null counts
null_counts = df.isnull().sum()
null_counts = null_counts[null_counts > 0].sort_values(ascending=False)

print("\n" + "=" * 70)
print("NULL VALUE BREAKDOWN BY COLUMN")
print("=" * 70)

print(f"\n{'Column':<30} {'Nulls':<10} {'Reason'}")
print("-" * 70)

# Analyze each column with nulls
explanations = {}

# Rolling window features - BEGINNING OF TIME SERIES
explanations['r_3M'] = {
    'nulls': null_counts.get('r_3M', 0),
    'reason': '3-month (63-day) rolling return needs 63 previous days',
    'location': 'First 63 days per stock',
    'fixable': 'Yes - remove rows or accept NaN for early dates'
}

explanations['r_1M'] = {
    'nulls': null_counts.get('r_1M', 0),
    'reason': '1-month (21-day) rolling return needs 21 previous days',
    'location': 'First 21 days per stock',
    'fixable': 'Yes - remove rows or accept NaN for early dates'
}

explanations['r_1W'] = {
    'nulls': null_counts.get('r_1W', 0),
    'reason': '1-week (5-day) rolling return needs 5 previous days',
    'location': 'First 5 days per stock',
    'fixable': 'Yes - remove rows or accept NaN for early dates'
}

# Forward-looking features - END OF TIME SERIES
explanations['stock_fwd_ret_21d'] = {
    'nulls': null_counts.get('stock_fwd_ret_21d', 0),
    'reason': 'Forward 21-day return needs 21 FUTURE days',
    'location': 'Last 21 days per stock (no future data available)',
    'fixable': 'No - these rows cannot be used for training (no label)'
}

explanations['sp500_fwd_ret_21d'] = {
    'nulls': null_counts.get('sp500_fwd_ret_21d', 0),
    'reason': 'Forward 21-day return needs 21 FUTURE days',
    'location': 'Last 21 days (no future data available)',
    'fixable': 'No - these rows cannot be used for training'
}

# Daily return - FIRST ROW PER STOCK
explanations['daily_return'] = {
    'nulls': null_counts.get('daily_return', 0),
    'reason': 'Daily return = pct_change() - needs previous day',
    'location': 'First day per stock (no previous day)',
    'fixable': 'Yes - remove first row per stock or set to 0'
}

# Volatility - NEEDS RETURNS
explanations['vol_1M'] = {
    'nulls': null_counts.get('vol_1M', 0),
    'reason': 'Volatility = std(daily_return) - needs returns',
    'location': 'Days where daily_return is null',
    'fixable': 'Yes - dependent on daily_return fix'
}

# Volume z-score - NEEDS VOLUME HISTORY
explanations['vol_z'] = {
    'nulls': null_counts.get('vol_z', 0),
    'reason': 'Volume z-score needs 20-day rolling window',
    'location': 'First 20 days per stock',
    'fixable': 'Yes - remove rows or accept NaN'
}

# SP500 features - FIRST DATE
explanations['sp500_daily_return'] = {
    'nulls': null_counts.get('sp500_daily_return', 0),
    'reason': 'SP500 daily return = pct_change() - needs previous day',
    'location': 'First date in dataset',
    'fixable': 'Yes - set to 0 or remove'
}

explanations['sp500_vol_1M'] = {
    'nulls': null_counts.get('sp500_vol_1M', 0),
    'reason': 'SP500 volatility needs 21 days of returns',
    'location': 'First ~21 days',
    'fixable': 'Yes - dependent on sp500_daily_return'
}

# Derived features
explanations['relative_return'] = {
    'nulls': null_counts.get('relative_return', 0),
    'reason': 'relative_return = daily_return - sp500_daily_return',
    'location': 'Where either component is null',
    'fixable': 'Yes - dependent on component fixes'
}

explanations['volatility_ratio'] = {
    'nulls': null_counts.get('volatility_ratio', 0),
    'reason': 'volatility_ratio = vol_1M / sp500_vol_1M',
    'location': 'Where either component is null',
    'fixable': 'Yes - dependent on component fixes'
}

# Macro features - FIRST DATE
explanations['CPI_chg'] = {
    'nulls': null_counts.get('CPI_chg', 0),
    'reason': 'CPI change = pct_change() - needs previous value',
    'location': 'First date (no previous CPI value)',
    'fixable': 'Yes - set to 0 or remove'
}

explanations['FedFunds_chg'] = {
    'nulls': null_counts.get('FedFunds_chg', 0),
    'reason': 'Fed Funds change = diff() - needs previous value',
    'location': 'First date (no previous Fed Funds value)',
    'fixable': 'Yes - set to 0 or remove'
}

# Print explanations
for col in null_counts.index:
    if col in explanations:
        exp = explanations[col]
        print(f"{col:<30} {exp['nulls']:<10} {exp['reason']}")
        print(f"{'':<30} {'':<10} Location: {exp['location']}")
        print(f"{'':<30} {'':<10} Fixable: {exp['fixable']}")
    else:
        print(f"{col:<30} {null_counts[col]:<10} Unknown reason")

# ========== DETAILED EXAMPLES ==========
print("\n" + "=" * 70)
print("DETAILED EXAMPLES")
print("=" * 70)

# Example 1: First rows (missing rolling windows)
print("\n1. EXAMPLE: First rows (missing rolling window features)")
print("-" * 70)
first_rows = df[df['stock'] == 'GOOGL'].head(10)
print(f"\nFirst 10 rows of GOOGL:")
print(f"{'Date':<12} {'r_1W':<10} {'r_1M':<10} {'r_3M':<10} {'daily_return':<12}")
print("-" * 70)
for idx, row in first_rows.iterrows():
    date = row['Date'].strftime('%Y-%m-%d')
    r1w = f"{row['r_1W']:.6f}" if pd.notna(row['r_1W']) else "NaN"
    r1m = f"{row['r_1M']:.6f}" if pd.notna(row['r_1M']) else "NaN"
    r3m = f"{row['r_3M']:.6f}" if pd.notna(row['r_3M']) else "NaN"
    daily_ret = f"{row['daily_return']:.6f}" if pd.notna(row['daily_return']) else "NaN"
    print(f"{date:<12} {r1w:<10} {r1m:<10} {r3m:<10} {daily_ret:<12}")

print("\nExplanation:")
print("  - Row 1 (2004-08-19): First day, no previous data")
print("    → daily_return = NaN (no previous close)")
print("    → r_1W = NaN (needs 5 previous days)")
print("    → r_1M = NaN (needs 21 previous days)")
print("    → r_3M = NaN (needs 63 previous days)")
print("  - Row 6 (2004-08-26): Has 5+ days of history")
print("    → r_1W available (has 5 previous days)")
print("    → r_1M still NaN (needs 21 days)")
print("    → r_3M still NaN (needs 63 days)")

# Example 2: Last rows (missing forward returns)
print("\n2. EXAMPLE: Last rows (missing forward return/label)")
print("-" * 70)
last_rows = df[df['stock'] == 'GOOGL'].tail(10)
print(f"\nLast 10 rows of GOOGL:")
print(f"{'Date':<12} {'stock_fwd_ret_21d':<20} {'y':<10}")
print("-" * 70)
for idx, row in last_rows.iterrows():
    date = row['Date'].strftime('%Y-%m-%d')
    fwd_ret = f"{row['stock_fwd_ret_21d']:.6f}" if pd.notna(row['stock_fwd_ret_21d']) else "NaN"
    y_val = f"{row['y']:.0f}" if pd.notna(row['y']) else "NaN"
    print(f"{date:<12} {fwd_ret:<20} {y_val:<10}")

print("\nExplanation:")
print("  - Last 21 days cannot compute forward returns")
print("  - Need Close price 21 days in the future (not available)")
print("  - Therefore, y (label) is also NaN")
print("  - These rows CANNOT be used for training (no target variable)")

# ========== NULL LOCATION SUMMARY ==========
print("\n" + "=" * 70)
print("NULL LOCATION SUMMARY")
print("=" * 70)

# Check where nulls occur
print("\nNulls at START of time series (rolling windows):")
start_nulls = {}
for col in ['r_1W', 'r_1M', 'r_3M', 'vol_z']:
    if col in df.columns:
        first_non_null_idx = df[col].first_valid_index()
        if first_non_null_idx is not None:
            first_non_null_date = df.loc[first_non_null_idx, 'Date']
            null_count_before = df.loc[:first_non_null_idx, col].isna().sum()
            print(f"  {col}: First valid at {first_non_null_date}, {null_count_before} nulls before")

print("\nNulls at END of time series (forward returns):")
end_nulls = {}
for col in ['stock_fwd_ret_21d', 'sp500_fwd_ret_21d', 'y']:
    if col in df.columns:
        last_non_null_idx = df[col].last_valid_index()
        if last_non_null_idx is not None:
            last_non_null_date = df.loc[last_non_null_idx, 'Date']
            null_count_after = df.loc[last_non_null_idx:, col].isna().sum()
            print(f"  {col}: Last valid at {last_non_null_date}, {null_count_after} nulls after")

# ========== RECOMMENDATIONS ==========
print("\n" + "=" * 70)
print("RECOMMENDATIONS FOR HANDLING NULLS")
print("=" * 70)

print("\n1. REMOVE rows with null labels (y is NaN):")
print("   - These are the last 21 days per stock")
print("   - Cannot be used for training (no target variable)")
print("   - Rows to remove: ~42 (21 days × 2 stocks)")

print("\n2. HANDLE missing features at start:")
print("   Option A: Remove first 63 rows (to get all r_3M values)")
print("   Option B: Forward fill or interpolate")
print("   Option C: Keep nulls and let model handle (some models support NaN)")

print("\n3. HANDLE first-day nulls (daily_return, CPI_chg, etc.):")
print("   - Set to 0 (no change on first day)")
print("   - Or remove first row per stock/date")

print("\n4. FINAL DATASET SIZE:")
total_rows = len(df)
rows_with_complete_labels = df['y'].notna().sum()
rows_with_all_features = df.drop(columns=['stock_fwd_ret_21d', 'sp500_fwd_ret_21d']).notna().all(axis=1).sum()
rows_for_training = df.drop(columns=['stock_fwd_ret_21d', 'sp500_fwd_ret_21d', 'y']).notna().all(axis=1) & df['y'].notna()

print(f"   - Total rows: {total_rows:,}")
print(f"   - Rows with labels (y): {rows_with_complete_labels:,}")
print(f"   - Rows with all features: {rows_with_all_features:,}")
print(f"   - Rows ready for training: {rows_for_training.sum():,}")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)

