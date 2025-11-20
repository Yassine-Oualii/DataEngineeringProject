"""
Detailed Outlier Examples
"""

import pandas as pd
import numpy as np

df = pd.read_csv('data/integrated_prepared_data.csv')
df['Date'] = pd.to_datetime(df['Date'])

print("=" * 70)
print("DETAILED OUTLIER EXAMPLES")
print("=" * 70)

# Example 1: VIX Crisis Outlier
print("\nEXAMPLE 1: VIX Outlier - Financial Crisis 2008")
print("-" * 70)
crisis_row = df[df['Date'] == '2008-10-07'].iloc[0]
print(f"\nDate: 2008-10-07")
print(f"Stock: {crisis_row['stock']}")
print(f"VIX: {crisis_row['VIX']:.2f}")
print(f"Close: ${crisis_row['Close']:.2f}")
print(f"SP500 Close: ${crisis_row['sp500_Close']:.2f}")
print(f"\nContext: Peak of 2008 Financial Crisis")
print("VIX > 50 indicates extreme market panic")

# Calculate Z-score
vix_mean = df['VIX'].mean()
vix_std = df['VIX'].std()
vix_zscore = abs((crisis_row['VIX'] - vix_mean) / vix_std)
print(f"\nZ-Score: {vix_zscore:.2f} (mean: {vix_mean:.2f}, std: {vix_std:.2f})")

# Example 2: Volume IPO Outlier
print("\n" + "=" * 70)
print("EXAMPLE 2: Volume Outlier - GOOGL IPO Day")
print("-" * 70)
ipo_row = df[(df['Date'] == '2004-08-19') & (df['stock'] == 'GOOGL')].iloc[0]
print(f"\nDate: 2004-08-19")
print(f"Stock: {ipo_row['stock']}")
print(f"Volume: {ipo_row['Volume']:,}")
print(f"Close: ${ipo_row['Close']:.2f}")
print(f"\nContext: GOOGL Initial Public Offering")
print("IPOs typically have extremely high trading volume")

vol_mean = df['Volume'].mean()
vol_std = df['Volume'].std()
vol_zscore = abs((ipo_row['Volume'] - vol_mean) / vol_std)
print(f"\nZ-Score: {vol_zscore:.2f} (mean: {vol_mean:,.0f}, std: {vol_std:,.0f})")
print(f"Volume is {vol_zscore:.1f}x the standard deviation above mean")

# Example 3: High Price Outlier - Recent META
print("\n" + "=" * 70)
print("EXAMPLE 3: Price Outlier - Recent META High")
print("-" * 70)
high_price_row = df[(df['Date'] == '2024-09-23') & (df['stock'] == 'META')].iloc[0]
print(f"\nDate: 2024-09-23")
print(f"Stock: {high_price_row['stock']}")
print(f"Close: ${high_price_row['Close']:.2f}")
print(f"High: ${high_price_row['High']:.2f}")
print(f"Low: ${high_price_row['Low']:.2f}")
print(f"Volume: {high_price_row['Volume']:,}")
print(f"\nContext: Recent high price (2024)")
print("Reflects stock price growth over 20 years")

close_mean = df['Close'].mean()
close_std = df['Close'].std()
close_zscore = abs((high_price_row['Close'] - close_mean) / close_std)
print(f"\nZ-Score: {close_zscore:.2f} (mean: ${close_mean:.2f}, std: ${close_std:.2f})")

# Compare with historical GOOGL price same date
googl_same_date = df[(df['Date'] == '2024-09-23') & (df['stock'] == 'GOOGL')]
if len(googl_same_date) > 0:
    print(f"\nComparison - GOOGL same date: ${googl_same_date.iloc[0]['Close']:.2f}")

print("\n" + "=" * 70)
print("OUTLIER SUMMARY")
print("=" * 70)
print("\nKey Insights:")
print("1. VIX outliers capture market crisis periods (2008 Financial Crisis)")
print("2. Volume outliers capture IPO days and major events")
print("3. Price outliers reflect long-term stock growth")
print("4. Most outliers are VALID extreme events, not data errors")

