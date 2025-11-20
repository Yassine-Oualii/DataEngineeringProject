"""
Concrete Examples of Null Value Filling

Shows exactly how each null value was filled with step-by-step explanation.
"""

import pandas as pd

# Load original data
df_original = pd.read_csv('data/integrated_raw_data.csv')
df_original['Date'] = pd.to_datetime(df_original['Date'])
df_original = df_original.sort_values(['stock', 'Date']).reset_index(drop=True)

# Load prepared data
df_prepared = pd.read_csv('data/integrated_prepared_data.csv')
df_prepared['Date'] = pd.to_datetime(df_prepared['Date'])
df_prepared = df_prepared.sort_values(['stock', 'Date']).reset_index(drop=True)

print("=" * 70)
print("CONCRETE EXAMPLES OF NULL VALUE FILLING")
print("=" * 70)

# ========== EXAMPLE 1: CPI ==========
print("\n" + "=" * 70)
print("EXAMPLE 1: CPI (Consumer Price Index)")
print("=" * 70)

# Find first row where CPI was null
googl_original = df_original[df_original['stock'] == 'GOOGL'].sort_values('Date').reset_index(drop=True)
null_cpi_row = googl_original[googl_original['CPI'].isnull()].iloc[0]
null_cpi_idx = googl_original[googl_original['CPI'].isnull()].index[0]

print(f"\nRow with NULL CPI:")
print(f"  Row Index: {null_cpi_idx}")
print(f"  Date: {null_cpi_row['Date'].strftime('%Y-%m-%d')}")
print(f"  Stock: {null_cpi_row['stock']}")
print(f"  CPI value: NULL (empty)")

# Find the next non-null CPI value
next_valid_cpi = googl_original[googl_original.index > null_cpi_idx]
next_valid_cpi = next_valid_cpi[next_valid_cpi['CPI'].notna()].iloc[0]

print(f"\nNext available CPI value (used for filling):")
print(f"  Row Index: {next_valid_cpi.name}")
print(f"  Date: {next_valid_cpi['Date'].strftime('%Y-%m-%d')}")
print(f"  CPI value: {next_valid_cpi['CPI']:.2f}")

# Show what happened
prepared_row = df_prepared[(df_prepared['stock'] == 'GOOGL') & 
                           (df_prepared['Date'] == null_cpi_row['Date'])].iloc[0]

print(f"\nAfter backward fill:")
print(f"  Date: {prepared_row['Date'].strftime('%Y-%m-%d')}")
print(f"  CPI value: {prepared_row['CPI']:.2f}")

print(f"\n📝 EXPLANATION (Step by Step):")
print(f"  1. We found a NULL value in CPI column on {null_cpi_row['Date'].strftime('%Y-%m-%d')}")
print(f"  2. We looked FORWARD in time (later dates) within the same stock (GOOGL)")
print(f"  3. We found the next available CPI value on {next_valid_cpi['Date'].strftime('%Y-%m-%d')}: {next_valid_cpi['CPI']:.2f}")
print(f"  4. We 'backward filled' - meaning we took that future value and used it to fill the past null")
print(f"  5. Result: {null_cpi_row['Date'].strftime('%Y-%m-%d')} now has CPI = {prepared_row['CPI']:.2f}")
print(f"  6. Why this works: CPI is monthly macro data, so it's reasonable to use the next month's value")

# ========== EXAMPLE 2: GDP ==========
print("\n" + "=" * 70)
print("EXAMPLE 2: GDP (Gross Domestic Product)")
print("=" * 70)

# Find first row where GDP was null
null_gdp_row = googl_original[googl_original['GDP'].isnull()].iloc[0]
null_gdp_idx = googl_original[googl_original['GDP'].isnull()].index[0]

print(f"\nRow with NULL GDP:")
print(f"  Row Index: {null_gdp_idx}")
print(f"  Date: {null_gdp_row['Date'].strftime('%Y-%m-%d')}")
print(f"  Stock: {null_gdp_row['stock']}")
print(f"  GDP value: NULL (empty)")

# Find the next non-null GDP value
next_valid_gdp = googl_original[googl_original.index > null_gdp_idx]
next_valid_gdp = next_valid_gdp[next_valid_gdp['GDP'].notna()].iloc[0]

print(f"\nNext available GDP value (used for filling):")
print(f"  Row Index: {next_valid_gdp.name}")
print(f"  Date: {next_valid_gdp['Date'].strftime('%Y-%m-%d')}")
print(f"  GDP value: {next_valid_gdp['GDP']:.2f}")

# Show what happened
prepared_gdp_row = df_prepared[(df_prepared['stock'] == 'GOOGL') & 
                               (df_prepared['Date'] == null_gdp_row['Date'])].iloc[0]

print(f"\nAfter backward fill:")
print(f"  Date: {prepared_gdp_row['Date'].strftime('%Y-%m-%d')}")
print(f"  GDP value: {prepared_gdp_row['GDP']:.2f}")

# Calculate days between
days_diff = (next_valid_gdp['Date'] - null_gdp_row['Date']).days

print(f"\n📝 EXPLANATION (Step by Step):")
print(f"  1. We found a NULL value in GDP column on {null_gdp_row['Date'].strftime('%Y-%m-%d')}")
print(f"  2. We looked FORWARD in time ({days_diff} days later) within the same stock (GOOGL)")
print(f"  3. We found the next available GDP value on {next_valid_gdp['Date'].strftime('%Y-%m-%d')}: {next_valid_gdp['GDP']:.2f}")
print(f"  4. We used 'backward fill' method: took that future value and filled the past null")
print(f"  5. Result: {null_gdp_row['Date'].strftime('%Y-%m-%d')} now has GDP = {prepared_gdp_row['GDP']:.2f}")
print(f"  6. Why this works: GDP is quarterly macro data, so using next quarter's value is appropriate")

# ========== EXAMPLE 3: Unemployment_Rate ==========
print("\n" + "=" * 70)
print("EXAMPLE 3: Unemployment_Rate")
print("=" * 70)

# Find first row where Unemployment_Rate was null
null_unemp_row = googl_original[googl_original['Unemployment_Rate'].isnull()].iloc[0]
null_unemp_idx = googl_original[googl_original['Unemployment_Rate'].isnull()].index[0]

print(f"\nRow with NULL Unemployment_Rate:")
print(f"  Row Index: {null_unemp_idx}")
print(f"  Date: {null_unemp_row['Date'].strftime('%Y-%m-%d')}")
print(f"  Stock: {null_unemp_row['stock']}")
print(f"  Unemployment_Rate value: NULL (empty)")

# Find the next non-null Unemployment_Rate value
next_valid_unemp = googl_original[googl_original.index > null_unemp_idx]
next_valid_unemp = next_valid_unemp[next_valid_unemp['Unemployment_Rate'].notna()].iloc[0]

print(f"\nNext available Unemployment_Rate value (used for filling):")
print(f"  Row Index: {next_valid_unemp.name}")
print(f"  Date: {next_valid_unemp['Date'].strftime('%Y-%m-%d')}")
print(f"  Unemployment_Rate value: {next_valid_unemp['Unemployment_Rate']:.2f}")

# Show what happened
prepared_unemp_row = df_prepared[(df_prepared['stock'] == 'GOOGL') & 
                                 (df_prepared['Date'] == null_unemp_row['Date'])].iloc[0]

print(f"\nAfter backward fill:")
print(f"  Date: {prepared_unemp_row['Date'].strftime('%Y-%m-%d')}")
print(f"  Unemployment_Rate value: {prepared_unemp_row['Unemployment_Rate']:.2f}")

# Calculate days between
days_diff = (next_valid_unemp['Date'] - null_unemp_row['Date']).days

print(f"\n📝 EXPLANATION (Step by Step):")
print(f"  1. We found a NULL value in Unemployment_Rate column on {null_unemp_row['Date'].strftime('%Y-%m-%d')}")
print(f"  2. We looked FORWARD in time ({days_diff} days later) within the same stock (GOOGL)")
print(f"  3. We found the next available Unemployment_Rate value on {next_valid_unemp['Date'].strftime('%Y-%m-%d')}: {next_valid_unemp['Unemployment_Rate']:.2f}%")
print(f"  4. We used 'backward fill' method: took that future value and filled the past null")
print(f"  5. Result: {null_unemp_row['Date'].strftime('%Y-%m-%d')} now has Unemployment_Rate = {prepared_unemp_row['Unemployment_Rate']:.2f}%")
print(f"  6. Why this works: Unemployment rate is monthly macro data, relatively stable month-to-month")

# ========== SUMMARY ==========
print("\n" + "=" * 70)
print("SUMMARY OF FILLING METHOD")
print("=" * 70)

print("""
Method Used: Backward Fill (bfill) - Grouped by Stock

How it works:
  1. For each NULL value, look FORWARD in time (later dates)
  2. Find the next available (non-null) value in the same column
  3. Copy that future value back to fill the null
  4. Process is done separately for each stock (GOOGL, META)

Why Backward Fill (not Forward Fill)?
  - Nulls are at the START of the time series (GOOGL IPO date: 2004-08-19)
  - Forward fill needs a previous value (doesn't exist before IPO)
  - Backward fill uses the next available value (exists after IPO)
  
Why Grouped by Stock?
  - Each stock has its own time series
  - Prevents mixing values between different stocks
  - Maintains data integrity

Why This Method is Appropriate:
  - Macro economic indicators (CPI, GDP, Unemployment) are:
    * Same for all stocks on the same date (market-wide)
    * Published monthly/quarterly (forward-filled to daily)
    * Relatively stable over short periods
  - Using next month's value for early dates is reasonable
  - Better than dropping rows (would lose IPO period data)
""")

# ========== VISUAL COMPARISON ==========
print("\n" + "=" * 70)
print("VISUAL COMPARISON")
print("=" * 70)

print("\nBefore (integrated_raw_data.csv):")
comparison_dates = [null_cpi_row['Date'], null_gdp_row['Date'], null_unemp_row['Date']]
for date in comparison_dates[:1]:  # Show first example
    orig_row = df_original[(df_original['stock'] == 'GOOGL') & 
                           (df_original['Date'] == date)].iloc[0]
    print(f"  {date.strftime('%Y-%m-%d')}:")
    print(f"    CPI: {orig_row['CPI'] if pd.notna(orig_row['CPI']) else 'NULL'}")
    print(f"    GDP: {orig_row['GDP'] if pd.notna(orig_row['GDP']) else 'NULL'}")
    print(f"    Unemployment_Rate: {orig_row['Unemployment_Rate'] if pd.notna(orig_row['Unemployment_Rate']) else 'NULL'}")

print("\nAfter (integrated_prepared_data.csv):")
for date in comparison_dates[:1]:  # Show first example
    prep_row = df_prepared[(df_prepared['stock'] == 'GOOGL') & 
                           (df_prepared['Date'] == date)].iloc[0]
    print(f"  {date.strftime('%Y-%m-%d')}:")
    print(f"    CPI: {prep_row['CPI']:.2f} ✓")
    print(f"    GDP: {prep_row['GDP']:.2f} ✓")
    print(f"    Unemployment_Rate: {prep_row['Unemployment_Rate']:.2f}% ✓")

print("\n" + "=" * 70)

