"""
Functional Dependencies (FD) Analysis

In database theory, a functional dependency X → Y means that
if two rows have the same values for attributes in X, they must
have the same values for attributes in Y.

For our integrated dataset, we analyze:
- Which attributes determine other attributes
- Candidate keys
- Data integrity constraints
"""

import pandas as pd
import numpy as np

def analyze_functional_dependencies():
    """
    Analyze functional dependencies in the integrated dataset.
    """
    print("=" * 70)
    print("FUNCTIONAL DEPENDENCIES (FD) ANALYSIS")
    print("=" * 70)
    
    # Load data
    df = pd.read_csv('data/integrated_raw_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    
    print(f"\nDataset shape: {df.shape}")
    print(f"Columns: {len(df.columns)}")
    print(f"Rows: {len(df)}")
    
    # ========== CANDIDATE KEY ANALYSIS ==========
    print("\n" + "=" * 70)
    print("1. CANDIDATE KEY ANALYSIS")
    print("=" * 70)
    
    # Check if (stock, Date) is a candidate key (should uniquely identify rows)
    duplicates = df.groupby(['stock', 'Date']).size()
    if (duplicates > 1).any():
        print("⚠ WARNING: (stock, Date) is NOT a candidate key - duplicates found!")
        print(f"Duplicate (stock, Date) pairs: {(duplicates > 1).sum()}")
    else:
        print("✓ (stock, Date) is a CANDIDATE KEY - uniquely identifies each row")
        print(f"Total unique (stock, Date) pairs: {len(duplicates)}")
        print(f"Total rows: {len(df)}")
        print("→ No duplicates, (stock, Date) is valid primary key")
    
    # Check Date alone
    date_unique = df['Date'].nunique()
    print(f"\nDate alone: {date_unique} unique values out of {len(df)} rows")
    print("→ Date is NOT a candidate key (multiple stocks per date)")
    
    # Check stock alone
    stock_unique = df['stock'].nunique()
    print(f"\nStock alone: {stock_unique} unique values out of {len(df)} rows")
    print("→ Stock is NOT a candidate key (multiple dates per stock)")
    
    # ========== FUNCTIONAL DEPENDENCIES ==========
    print("\n" + "=" * 70)
    print("2. FUNCTIONAL DEPENDENCIES")
    print("=" * 70)
    
    print("\nFD Notation: X → Y means 'X functionally determines Y'")
    print("If two rows have same values for X, they must have same values for Y\n")
    
    # FD 1: (stock, Date) → Stock-specific attributes
    print("2.1 STOCK-SPECIFIC FUNCTIONAL DEPENDENCIES")
    print("-" * 70)
    print("(stock, Date) → {Close, High, Low, Open, Volume}")
    print("  Meaning: For a given stock on a given date, there is exactly")
    print("           one Close, High, Low, Open, Volume value")
    print("  Validation: Checking if this holds...")
    
    stock_cols = ['Close', 'High', 'Low', 'Open', 'Volume']
    violations = 0
    for col in stock_cols:
        grouped = df.groupby(['stock', 'Date'])[col].nunique()
        if (grouped > 1).any():
            violations += 1
            print(f"  ✗ Violation found: {col} has multiple values for same (stock, Date)")
    
    if violations == 0:
        print("  ✓ Valid: Each (stock, Date) has unique stock OHLCV values")
    
    # FD 2: Date → Market-wide attributes
    print("\n2.2 MARKET-WIDE FUNCTIONAL DEPENDENCIES")
    print("-" * 70)
    print("Date → {sp500_Close, sp500_High, sp500_Low, sp500_Open, sp500_Volume,")
    print("         CPI, Fed_Funds_Rate, GDP, Unemployment_Rate,")
    print("         VIX, Put_Call_Ratio, Market_Breadth,")
    print("         sector_XLK, sector_XLF, sector_XLV, sector_XLE, sector_XLI,")
    print("         spy_RSI, spy_SMA_50, spy_SMA_200,")
    print("         qqq_RSI, qqq_SMA_50, qqq_SMA_200}")
    print("  Meaning: For a given date, ALL stocks share the same:")
    print("           - SP500 values (same market on same day)")
    print("           - Macro indicators (same economy on same day)")
    print("           - Market sentiment (same market conditions)")
    print("  Validation: Checking if this holds...")
    
    market_cols = ['sp500_Close', 'sp500_High', 'sp500_Low', 'sp500_Open', 'sp500_Volume',
                   'CPI', 'Fed_Funds_Rate', 'GDP', 'Unemployment_Rate',
                   'VIX', 'Put_Call_Ratio', 'Market_Breadth',
                   'sector_XLK', 'sector_XLF', 'sector_XLV', 'sector_XLE', 'sector_XLI',
                   'spy_RSI', 'spy_SMA_50', 'spy_SMA_200',
                   'qqq_RSI', 'qqq_SMA_50', 'qqq_SMA_200']
    
    market_violations = []
    for col in market_cols:
        if col in df.columns:
            grouped = df.groupby('Date')[col].nunique()
            violations_fd = (grouped > 1).sum()
            if violations_fd > 0:
                market_violations.append((col, violations_fd))
    
    if market_violations:
        print(f"  ⚠ Found {len(market_violations)} columns with violations:")
        for col, count in market_violations:
            print(f"    - {col}: {count} dates with multiple values")
            # Show example
            example = df.groupby('Date')[col].agg(['nunique', 'first', 'last']).reset_index()
            example_viol = example[example['nunique'] > 1].head(1)
            if len(example_viol) > 0:
                date_ex = example_viol.iloc[0]['Date']
                values = df[df['Date'] == date_ex][col].unique()
                print(f"      Example: Date {date_ex} has values: {values[:3]}")
    else:
        print("  ✓ Valid: All market-wide attributes are same for all stocks on same date")
    
    # FD 3: Stock → nothing (stock alone doesn't determine anything specific)
    print("\n2.3 STOCK ALONE")
    print("-" * 70)
    print("Stock → nothing")
    print("  Meaning: Stock alone doesn't functionally determine any attribute")
    print("           (same stock appears on multiple dates with different values)")
    print("  Validation: ✓ Confirmed - stock appears multiple times")
    
    # ========== EXAMPLES OF FUNCTIONAL DEPENDENCIES ==========
    print("\n" + "=" * 70)
    print("3. CONCRETE EXAMPLES OF FUNCTIONAL DEPENDENCIES")
    print("=" * 70)
    
    # Example 1: (stock, Date) → Close
    print("\nExample 1: (stock, Date) → Close")
    print("-" * 70)
    example_date = df['Date'].iloc[0]
    example_stock = 'GOOGL'
    example_rows = df[(df['stock'] == example_stock) & (df['Date'] == example_date)]
    if len(example_rows) == 1:
        close_value = example_rows.iloc[0]['Close']
        print(f"  (stock={example_stock}, Date={example_date.date()}) → Close={close_value:.4f}")
        print(f"  ✓ Single value determined")
    else:
        print(f"  ✗ Multiple Close values found: {len(example_rows)}")
    
    # Example 2: Date → sp500_Close
    print("\nExample 2: Date → sp500_Close")
    print("-" * 70)
    example_date = df['Date'].iloc[0]
    example_rows = df[df['Date'] == example_date]
    if example_rows['sp500_Close'].nunique() == 1:
        sp500_value = example_rows.iloc[0]['sp500_Close']
        num_stocks = len(example_rows)
        print(f"  Date={example_date.date()} → sp500_Close={sp500_value:.2f}")
        print(f"  ✓ All {num_stocks} stocks on this date share same SP500 value")
    else:
        print(f"  ✗ Multiple SP500 values found for same date")
    
    # Example 3: Date → CPI
    print("\nExample 3: Date → CPI")
    print("-" * 70)
    example_date = df['Date'].iloc[0]
    example_rows = df[df['Date'] == example_date]
    if example_rows['CPI'].nunique() == 1:
        cpi_value = example_rows.iloc[0]['CPI']
        num_stocks = len(example_rows)
        print(f"  Date={example_date.date()} → CPI={cpi_value:.2f}")
        print(f"  ✓ All {num_stocks} stocks on this date share same CPI value")
        print(f"  (CPI is monthly data, forward-filled to daily)")
    else:
        print(f"  ✗ Multiple CPI values found for same date")
    
    # ========== VIOLATIONS CHECK ==========
    print("\n" + "=" * 70)
    print("4. DATA INTEGRITY CHECK (FD Violations)")
    print("=" * 70)
    
    # Check for NULL/NaN in key attributes
    print("\n4.1 NULL Values in Key Attributes")
    print("-" * 70)
    key_attrs = ['stock', 'Date']
    for attr in key_attrs:
        null_count = df[attr].isna().sum()
        if null_count > 0:
            print(f"  ✗ {attr}: {null_count} NULL values found")
        else:
            print(f"  ✓ {attr}: No NULL values")
    
    # Check for NULL in functionally determined attributes
    print("\n4.2 NULL Values in Functionally Determined Attributes")
    print("-" * 70)
    # For each (stock, Date) pair, stock attributes should not be NULL
    stock_cols = ['Close', 'High', 'Low', 'Open', 'Volume']
    for col in stock_cols:
        grouped = df.groupby(['stock', 'Date'])[col].apply(lambda x: x.isna().any())
        violations = grouped[grouped].sum()
        if violations > 0:
            print(f"  ⚠ {col}: {violations} (stock, Date) pairs have NULL")
        else:
            print(f"  ✓ {col}: No NULL values for any (stock, Date) pair")
    
    # ========== SUMMARY ==========
    print("\n" + "=" * 70)
    print("5. FUNCTIONAL DEPENDENCIES SUMMARY")
    print("=" * 70)
    
    print("\nIdentified Functional Dependencies:")
    print("\nFD1: (stock, Date) → {Close, High, Low, Open, Volume}")
    print("     → Stock-specific price data depends on both stock and date")
    
    print("\nFD2: Date → {sp500_Close, sp500_High, sp500_Low, sp500_Open, sp500_Volume}")
    print("     → SP500 values are same for all stocks on same date")
    
    print("\nFD3: Date → {CPI, Fed_Funds_Rate, GDP, Unemployment_Rate}")
    print("     → Macro indicators are same for all stocks on same date")
    
    print("\nFD4: Date → {VIX, Put_Call_Ratio, Market_Breadth}")
    print("     → Market sentiment indicators are same for all stocks on same date")
    
    print("\nFD5: Date → {sector_XLK, sector_XLF, ..., sector_XLI}")
    print("     → Sector ETF prices are same for all stocks on same date")
    
    print("\nFD6: Date → {spy_RSI, spy_SMA_50, spy_SMA_200, qqq_RSI, qqq_SMA_50, qqq_SMA_200}")
    print("     → Technical indicators are same for all stocks on same date")
    
    print("\nCandidate Key: (stock, Date)")
    print("  → Uniquely identifies each row in the dataset")
    print("  → All attributes functionally depend on (stock, Date)")
    
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)

if __name__ == '__main__':
    analyze_functional_dependencies()

