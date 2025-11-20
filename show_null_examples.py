"""
Show concrete examples of null data cases
"""
import pandas as pd

df = pd.read_csv('data/integrated_raw_data.csv')
df['Date'] = pd.to_datetime(df['Date'])

print("=" * 70)
print("CONCRETE NULL DATA EXAMPLES")
print("=" * 70)

print("\n=== Example 1: First Row (GOOGL IPO Date) ===")
row = df.iloc[0]
print(f"Stock: {row['stock']}")
print(f"Date: {row['Date'].strftime('%Y-%m-%d')}")
print(f"Close: {row['Close']:.4f} ✓")
print(f"High: {row['High']:.4f} ✓")
print(f"CPI: {row['CPI']} ⚠ NULL")
print(f"GDP: {row['GDP']} ⚠ NULL")
print(f"Unemployment_Rate: {row['Unemployment_Rate']} ⚠ NULL")
print(f"SP500_Close: {row['sp500_Close']:.2f} ✓")
print(f"VIX: {row['VIX']:.2f} ✓")

print("\n=== Example 2: After Null Period ===")
clean_row = df[df['CPI'].notna()].iloc[0]
print(f"Stock: {clean_row['stock']}")
print(f"Date: {clean_row['Date'].strftime('%Y-%m-%d')}")
print(f"CPI: {clean_row['CPI']:.2f} ✓")
print(f"GDP: {clean_row['GDP']:.2f} ✓")
print(f"Unemployment_Rate: {clean_row['Unemployment_Rate']:.2f} ✓")

print("\n=== Example 3: Null Pattern Analysis ===")
googl_df = df[df['stock'] == 'GOOGL'].sort_values('Date')
null_period = googl_df[googl_df['CPI'].isnull()]
print(f"GOOGL null period: {len(null_period)} rows")
print(f"  From: {null_period['Date'].min().strftime('%Y-%m-%d')}")
print(f"  To: {null_period['Date'].max().strftime('%Y-%m-%d')}")
print(f"  Days: {(null_period['Date'].max() - null_period['Date'].min()).days + 1}")

print("\n=== Example 4: Comparison - META (No Nulls) ===")
meta_df = df[df['stock'] == 'META'].sort_values('Date')
first_meta = meta_df.iloc[0]
print(f"Stock: {first_meta['stock']}")
print(f"Date: {first_meta['Date'].strftime('%Y-%m-%d')}")
print(f"CPI: {first_meta['CPI']:.2f} ✓")
print(f"GDP: {first_meta['GDP']:.2f} ✓")
print(f"Unemployment_Rate: {first_meta['Unemployment_Rate']:.2f} ✓")
print("\nNote: META IPO (2012-05-18) has macro data available")

