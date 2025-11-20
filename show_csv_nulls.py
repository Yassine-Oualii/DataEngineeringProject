"""
Show how null values appear in CSV files
"""
import pandas as pd

df = pd.read_csv('data/integrated_raw_data.csv', nrows=10)

print("=" * 70)
print("HOW NULL VALUES APPEAR IN CSV FILES")
print("=" * 70)

print("\nIn CSV format, null values appear as EMPTY between commas")
print("Example: ,, means there's an empty/null value between two commas\n")

print("Row 0 (GOOGL IPO - has nulls):")
row0 = df.iloc[0]
print(f"  Date: {row0['Date']}")
print(f"  Stock: {row0['stock']}")
print(f"  Close: {row0['Close']}")
print(f"  CPI: '{row0['CPI']}' (type: {type(row0['CPI'])})")
print(f"  GDP: '{row0['GDP']}' (type: {type(row0['GDP'])})")
print(f"  Unemployment_Rate: '{row0['Unemployment_Rate']}'")

print("\n" + "-" * 70)
print("RAW CSV LINE (showing empty values):")
print("-" * 70)

# Read raw CSV line
with open('data/integrated_raw_data.csv', 'r') as f:
    lines = f.readlines()
    header = lines[0].strip().split(',')
    data_line = lines[1].strip().split(',')
    
    print("\nHeader positions:")
    for i, col in enumerate(header):
        if col in ['CPI', 'GDP', 'Unemployment_Rate']:
            print(f"  Position {i}: {col}")
    
    print("\nData row 1 (index 0 in CSV):")
    cpi_idx = header.index('CPI')
    gdp_idx = header.index('GDP')
    unemp_idx = header.index('Unemployment_Rate')
    
    print(f"  Position {cpi_idx} (CPI): '{data_line[cpi_idx]}'")
    print(f"  Position {gdp_idx} (GDP): '{data_line[gdp_idx]}'")
    print(f"  Position {unemp_idx} (Unemployment_Rate): '{data_line[unemp_idx]}'")
    
    print("\nNotice: Empty strings '' represent NULL in CSV!")

print("\n" + "-" * 70)
print("PANDAS INTERPRETATION:")
print("-" * 70)

print("\nWhen pandas reads the CSV:")
print(f"  df['CPI'].iloc[0] = {repr(df.iloc[0]['CPI'])}")
print(f"  Type: {type(df.iloc[0]['CPI'])}")
print(f"  Is NaN: {pd.isna(df.iloc[0]['CPI'])}")
print(f"  Is None: {df.iloc[0]['CPI'] is None}")
print(f"  Equals empty string: {df.iloc[0]['CPI'] == ''}")

print("\n" + "-" * 70)
print("COMPARISON - Row with data (after null period):")
print("-" * 70)

# Find first row with non-null CPI
row_with_data = df[df['CPI'].notna()].iloc[0]
print(f"  Date: {row_with_data['Date']}")
print(f"  CPI: {row_with_data['CPI']} (valid number)")
print(f"  GDP: {row_with_data['GDP']} (may still be null)")
print(f"  Is CPI NaN: {pd.isna(row_with_data['CPI'])}")

print("\n" + "-" * 70)
print("VISUAL EXAMPLE FROM CSV:")
print("-" * 70)

print("\nRaw CSV format (row 1):")
print("...,893181924,GOOGL,1091.23,...,1249400000,,1.5,,,16.96...")
print("                                            ↑    ↑ ↑")
print("                                            CPI  GDP Unemp")
print("                                          (empty) (empty) (empty)")
print("\nThis means: CPI is NULL, GDP is NULL, Unemployment_Rate is NULL")

print("\n" + "=" * 70)
print("SUMMARY:")
print("=" * 70)
print("""
In CSV files:
  - NULL values appear as empty strings: ""
  - Visually: double commas ,, (nothing between commas)
  - When pandas reads CSV: empty strings become NaN/None

In your CSV editor:
  - You see: empty cells or nothing between commas
  - This IS the null value representation

In pandas:
  - pd.isna() or pd.isnull() detects these as null
  - They appear as NaN in DataFrames
""")

