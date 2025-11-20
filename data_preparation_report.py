"""
Data Preparation Report - Null Data Handling

Analyzes and documents all processes for dealing with null data
in the integrated dataset.
"""

import pandas as pd
import numpy as np

def analyze_null_data():
    """
    Comprehensive analysis of null data and preparation processes.
    """
    print("=" * 70)
    print("DATA PREPARATION REPORT - NULL DATA HANDLING")
    print("=" * 70)
    
    # Load data
    df = pd.read_csv('data/integrated_raw_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    
    print(f"\nDataset Overview:")
    print(f"  Total rows: {len(df):,}")
    print(f"  Total columns: {len(df.columns)}")
    print(f"  Total cells: {len(df) * len(df.columns):,}")
    
    # ========== NULL DETECTION ==========
    print("\n" + "=" * 70)
    print("1. NULL DETECTION ANALYSIS")
    print("=" * 70)
    
    null_counts = df.isnull().sum()
    null_percentages = (null_counts / len(df)) * 100
    null_data = pd.DataFrame({
        'Column': null_counts.index,
        'Null_Count': null_counts.values,
        'Null_Percentage': null_percentages.values
    })
    null_data = null_data[null_data['Null_Count'] > 0].sort_values('Null_Count', ascending=False)
    
    if len(null_data) > 0:
        print(f"\nFound {len(null_data)} columns with null values:")
        print("-" * 70)
        print(f"{'Column':<25} {'Null Count':<15} {'Percentage':<15}")
        print("-" * 70)
        for _, row in null_data.iterrows():
            print(f"{row['Column']:<25} {row['Null_Count']:<15} {row['Null_Percentage']:.2f}%")
        
        total_nulls = null_counts.sum()
        print("-" * 70)
        print(f"{'TOTAL':<25} {total_nulls:<15} {(total_nulls/(len(df)*len(df.columns))*100):.4f}%")
    else:
        print("\n✓ No null values found in the dataset!")
    
    # ========== NULL BY CATEGORY ==========
    print("\n" + "=" * 70)
    print("2. NULL VALUES BY DATA CATEGORY")
    print("=" * 70)
    
    categories = {
        'Stock Price Data': ['Close', 'High', 'Low', 'Open', 'Volume'],
        'SP500 Data': ['sp500_Close', 'sp500_High', 'sp500_Low', 'sp500_Open', 'sp500_Volume'],
        'Macro Indicators': ['CPI', 'Fed_Funds_Rate', 'GDP', 'Unemployment_Rate'],
        'Market Sentiment': ['VIX', 'Put_Call_Ratio', 'Market_Breadth'],
        'Sector ETFs': ['sector_XLK', 'sector_XLF', 'sector_XLV', 'sector_XLE', 'sector_XLI'],
        'Technical Indicators': ['spy_RSI', 'spy_SMA_50', 'spy_SMA_200', 'qqq_RSI', 'qqq_SMA_50', 'qqq_SMA_200']
    }
    
    for category, cols in categories.items():
        category_cols = [c for c in cols if c in df.columns]
        if category_cols:
            category_nulls = df[category_cols].isnull().sum().sum()
            category_pct = (category_nulls / (len(df) * len(category_cols))) * 100
            print(f"\n{category}:")
            print(f"  Columns: {len(category_cols)}")
            print(f"  Total nulls: {category_nulls}")
            print(f"  Percentage: {category_pct:.2f}%")
            
            # Show columns with nulls
            for col in category_cols:
                null_count = df[col].isnull().sum()
                if null_count > 0:
                    print(f"    - {col}: {null_count} nulls ({null_count/len(df)*100:.2f}%)")
    
    # ========== NULL PATTERNS ==========
    print("\n" + "=" * 70)
    print("3. NULL VALUE PATTERNS")
    print("=" * 70)
    
    # Check for rows with multiple nulls
    df['null_count'] = df.isnull().sum(axis=1)
    rows_with_nulls = df[df['null_count'] > 0]
    
    if len(rows_with_nulls) > 0:
        print(f"\nRows with null values: {len(rows_with_nulls)} ({len(rows_with_nulls)/len(df)*100:.2f}%)")
        print(f"Max nulls in a single row: {df['null_count'].max()}")
        print(f"Avg nulls per row (when nulls exist): {rows_with_nulls['null_count'].mean():.2f}")
        
        # Check null patterns by stock
        print("\nNull patterns by stock:")
        for stock in df['stock'].unique():
            stock_df = df[df['stock'] == stock]
            stock_nulls = stock_df.isnull().sum().sum()
            stock_pct = (stock_nulls / (len(stock_df) * len(df.columns))) * 100
            print(f"  {stock}: {stock_nulls} nulls ({stock_pct:.2f}%)")
        
        # Check null patterns by date
        print("\nNull patterns by date range:")
        date_null_counts = df.groupby('Date')['null_count'].sum()
        if len(date_null_counts[date_null_counts > 0]) > 0:
            print(f"  Dates with nulls: {len(date_null_counts[date_null_counts > 0])}")
            print(f"  First null date: {date_null_counts[date_null_counts > 0].index.min()}")
            print(f"  Last null date: {date_null_counts[date_null_counts > 0].index.max()}")
    else:
        print("\n✓ No null patterns detected - dataset is complete!")
    
    # ========== CONCRETE NULL EXAMPLES ==========
    print("\n" + "=" * 70)
    print("4. CONCRETE NULL EXAMPLES")
    print("=" * 70)
    
    if len(rows_with_nulls) > 0:
        # Example 1: Show rows with nulls
        print("\nExample 1: Rows with Null Values")
        print("-" * 70)
        example_rows = rows_with_nulls.head(5)
        for idx, row in example_rows.iterrows():
            null_cols = [col for col in df.columns if pd.isna(row[col])]
            print(f"\n  Row {idx} ({row['stock']}, {row['Date'].strftime('%Y-%m-%d')}):")
            print(f"    Null columns: {', '.join(null_cols)}")
            print(f"    Total nulls: {len(null_cols)}")
            # Show sample of null values
            for col in null_cols[:3]:
                print(f"      - {col}: NULL")
        
        # Example 2: Columns with most nulls
        print("\nExample 2: Columns with Most Null Values")
        print("-" * 70)
        top_nulls = null_data.head(5)
        for _, row in top_nulls.iterrows():
            col = row['Column']
            null_count = int(row['Null_Count'])
            # Find example row with null
            null_row = df[df[col].isnull()].iloc[0] if null_count > 0 else None
            if null_row is not None:
                print(f"\n  Column: {col}")
                print(f"    Null count: {null_count} ({row['Null_Percentage']:.2f}%)")
                print(f"    Example row: ({null_row['stock']}, {null_row['Date'].strftime('%Y-%m-%d')})")
                print(f"    Value: NULL")
        
        # Example 3: Missing data patterns
        print("\nExample 3: Missing Data Patterns")
        print("-" * 70)
        
        # Check if nulls are at start/end of time series
        for stock in df['stock'].unique():
            stock_df = df[df['stock'] == stock].sort_values('Date')
            stock_nulls = stock_df.isnull().any(axis=1)
            if stock_nulls.any():
                null_dates = stock_df[stock_nulls]['Date']
                print(f"\n  {stock}:")
                print(f"    First date: {stock_df['Date'].min().strftime('%Y-%m-%d')}")
                print(f"    Last date: {stock_df['Date'].max().strftime('%Y-%m-%d')}")
                print(f"    Dates with nulls: {len(null_dates)}")
                if len(null_dates) > 0:
                    print(f"    First null date: {null_dates.min().strftime('%Y-%m-%d')}")
                    print(f"    Last null date: {null_dates.max().strftime('%Y-%m-%d')}")
                    
                    # Check if nulls at start/end
                    first_date = stock_df['Date'].min()
                    last_date = stock_df['Date'].max()
                    if null_dates.min() == first_date:
                        print(f"    ⚠ Nulls at START of time series")
                    if null_dates.max() == last_date:
                        print(f"    ⚠ Nulls at END of time series")
    else:
        print("\n✓ No null examples to show - dataset is complete!")
    
    # ========== DATA PREPARATION PROCESSES ==========
    print("\n" + "=" * 70)
    print("5. DATA PREPARATION PROCESSES")
    print("=" * 70)
    
    print("\n5.1 Processes Applied During Integration")
    print("-" * 70)
    print("""
    During data integration (integrate_data.py), the following processes
    were applied to handle null/missing data:
    
    1. Forward-filling Macro Data:
       - CPI, GDP, Unemployment_Rate are monthly/quarterly
       - Forward-filled to daily frequency using .ffill()
       - Example: CPI value from Jan 1st fills all trading days in January
       
    2. Inner Join on Date:
       - Stock data and SP500 data merged with inner join
       - Only keeps dates where both have data
       - Prevents nulls from missing date alignment
       
    3. Left Join for Market Data:
       - Market indicators (VIX, sectors, technical) use left join
       - Missing values may remain if indicator not available on that date
       - Preserves all stock date combinations
    """)
    
    # ========== RECOMMENDED HANDLING STRATEGIES ==========
    print("\n5.2 Recommended Null Handling Strategies")
    print("-" * 70)
    
    if len(null_data) > 0:
        print("\nFor columns with null values:")
        
        for col in null_data['Column'].head(10):
            null_pct = null_data[null_data['Column'] == col]['Null_Percentage'].iloc[0]
            
            if 'CPI' in col or 'GDP' in col or 'Unemployment' in col:
                print(f"\n  {col} ({null_pct:.2f}% nulls):")
                print("    Strategy: Forward-fill (already applied)")
                print("    Reason: Monthly/quarterly data, same value for all days in period")
                print("    Action: No further action needed")
                
            elif 'SMA_200' in col or 'SMA_50' in col:
                print(f"\n  {col} ({null_pct:.2f}% nulls):")
                print("    Strategy: Accept nulls at beginning of time series")
                print("    Reason: Moving averages need N days of history")
                print("    Action: Drop rows with null or use window-aware processing")
                
            elif 'RSI' in col:
                print(f"\n  {col} ({null_pct:.2f}% nulls):")
                print("    Strategy: Accept nulls at beginning or forward-fill")
                print("    Reason: RSI calculation needs historical data")
                print("    Action: Check if nulls are at start, drop if needed")
                
            elif col in ['sp500_Close', 'VIX', 'Market_Breadth']:
                print(f"\n  {col} ({null_pct:.2f}% nulls):")
                print("    Strategy: Investigate missing dates")
                print("    Reason: Should be available for all trading days")
                print("    Action: Check data collection, forward-fill if appropriate")
            else:
                print(f"\n  {col} ({null_pct:.2f}% nulls):")
                print("    Strategy: Review data source")
                print("    Action: Investigate why missing, apply appropriate strategy")
    else:
        print("\n✓ No null handling needed - dataset is complete!")
    
    # ========== FEATURE ENGINEERING NULL HANDLING ==========
    print("\n5.3 Null Handling for Feature Engineering")
    print("-" * 70)
    print("""
    When engineering features, additional nulls will be created:
    
    1. Rolling Window Features:
       - MA20, MA50: First 20/50 rows will be null
       - volatility_21d: First 21 rows will be null
       - rolling_return_21d: First 21 rows will be null
       Strategy: Drop rows with null rolling features
       
    2. Forward Returns (Labels):
       - Last 21 rows will be null (no future data)
       Strategy: Keep separate, drop only for training
       
    3. Percentage Changes:
       - First row of each stock will be null (no previous value)
       Strategy: Drop first row or forward-fill with 0
       
    4. Grouped Operations:
       - Must group by 'stock' to prevent cross-stock contamination
       - Nulls created properly within each stock's time series
       Strategy: Use df.groupby('stock') before rolling operations
    """)
    
    # ========== SUMMARY ==========
    print("\n" + "=" * 70)
    print("6. SUMMARY")
    print("=" * 70)
    
    total_nulls = df.isnull().sum().sum()
    total_cells = len(df) * len(df.columns)
    null_percentage = (total_nulls / total_cells) * 100
    
    print(f"\nOverall Null Statistics:")
    print(f"  Total null values: {total_nulls:,}")
    print(f"  Total cells: {total_cells:,}")
    print(f"  Null percentage: {null_percentage:.4f}%")
    print(f"  Rows with nulls: {len(rows_with_nulls):,} ({len(rows_with_nulls)/len(df)*100:.2f}%)")
    
    if total_nulls == 0:
        print("\n✓ Dataset is complete - no null handling required!")
    else:
        print(f"\n⚠ Dataset contains {total_nulls:,} null values requiring handling")
        print("  See recommended strategies above for each column type")
    
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    
    return df, null_data

if __name__ == '__main__':
    df, null_data = analyze_null_data()
    
    # Save null analysis to CSV
    if len(null_data) > 0:
        null_data.to_csv('data/null_analysis.csv', index=False)
        print("\n✓ Null analysis saved to data/null_analysis.csv")

