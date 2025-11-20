"""
Concrete Examples of Function Dependencies

Shows actual examples from the integrated dataset demonstrating
how features depend on each other.
"""

import pandas as pd
import numpy as np

def show_concrete_examples():
    """
    Show concrete dependency examples using actual data.
    """
    print("=" * 70)
    print("CONCRETE DEPENDENCY EXAMPLES FROM ACTUAL DATA")
    print("=" * 70)
    
    # Load data
    df = pd.read_csv('data/integrated_raw_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df_googl = df[df['stock'] == 'GOOGL'].sort_values('Date').reset_index(drop=True)
    
    # ========== EXAMPLE 1: Daily Return Chain ==========
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Daily Return Dependency Chain")
    print("=" * 70)
    
    df_googl['daily_return'] = df_googl['Close'].pct_change()
    
    print("\nDaily return depends on CURRENT Close and PREVIOUS Close:")
    print("daily_return[t] = (Close[t] - Close[t-1]) / Close[t-1]")
    print("\n" + "-" * 70)
    print(f"{'Row':<4} {'Date':<12} {'Prev Close':<12} {'Curr Close':<12} {'daily_return':<12} {'Calculation'}")
    print("-" * 70)
    
    for i in range(1, min(6, len(df_googl))):
        prev_close = df_googl.iloc[i-1]['Close']
        curr_close = df_googl.iloc[i]['Close']
        dr = df_googl.iloc[i]['daily_return']
        calc = f"({curr_close:.4f} - {prev_close:.4f}) / {prev_close:.4f}"
        print(f"{i:<4} {df_googl.iloc[i]['Date'].strftime('%Y-%m-%d'):<12} "
              f"{prev_close:<12.4f} {curr_close:<12.4f} {dr:<12.4f} {calc}")
    
    # ========== EXAMPLE 2: MA Ratio Dependency ==========
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Moving Average Ratio Dependency")
    print("=" * 70)
    
    ma20 = df_googl['Close'].rolling(20).mean()
    df_googl['ma20_ratio'] = df_googl['Close'] / ma20
    
    print("\nma20_ratio depends on Close and MA20 (which depends on 20 previous Close values):")
    print("MA20[t] = mean(Close[t-19] to Close[t])")
    print("ma20_ratio[t] = Close[t] / MA20[t]")
    print("\n" + "-" * 70)
    print(f"{'Row':<4} {'Date':<12} {'Close':<12} {'MA20':<12} {'ma20_ratio':<12} {'Uses Rows'}")
    print("-" * 70)
    
    for i in range(20, min(25, len(df_googl))):
        close_val = df_googl.iloc[i]['Close']
        ma20_val = ma20.iloc[i]
        ratio = df_googl.iloc[i]['ma20_ratio']
        uses_rows = f"{i-19} to {i}"
        print(f"{i:<4} {df_googl.iloc[i]['Date'].strftime('%Y-%m-%d'):<12} "
              f"{close_val:<12.4f} {ma20_val:<12.4f} {ratio:<12.4f} {uses_rows}")
    
    # ========== EXAMPLE 3: Volatility Dependency Chain ==========
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Volatility Dependency Chain (Multi-Level)")
    print("=" * 70)
    
    # Step 1: daily_return (already computed)
    # Step 2: volatility from daily_return
    df_googl['volatility_21d'] = df_googl['daily_return'].rolling(21).std()
    
    print("\nVolatility has a 2-level dependency chain:")
    print("Level 1: Close → daily_return")
    print("Level 2: daily_return → volatility_21d")
    print("\n" + "-" * 70)
    print(f"{'Row':<4} {'Date':<12} {'Close':<12} {'daily_return':<12} {'volatility_21d':<12}")
    print("-" * 70)
    
    for i in range(21, min(26, len(df_googl))):
        close_val = df_googl.iloc[i]['Close']
        dr = df_googl.iloc[i]['daily_return']
        vol = df_googl.iloc[i]['volatility_21d']
        print(f"{i:<4} {df_googl.iloc[i]['Date'].strftime('%Y-%m-%d'):<12} "
              f"{close_val:<12.4f} {dr:<12.4f} {vol:<12.4f}")
    
    print(f"\nNote: volatility_21d at row {21} uses daily_return values from rows 0 to 21")
    
    # ========== EXAMPLE 4: Relative Return (Stock vs SP500) ==========
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Relative Return Dependency (Stock vs SP500)")
    print("=" * 70)
    
    df_googl['sp500_daily_return'] = df_googl['sp500_Close'].pct_change()
    df_googl['relative_return'] = df_googl['daily_return'] - df_googl['sp500_daily_return']
    
    print("\nRelative return depends on TWO independent chains:")
    print("Chain 1: Close → stock daily_return")
    print("Chain 2: sp500_Close → sp500_daily_return")
    print("Then: relative_return = stock_daily_return - sp500_daily_return")
    print("\n" + "-" * 70)
    print(f"{'Row':<4} {'Date':<12} {'Stock DR':<12} {'SP500 DR':<12} {'Relative':<12}")
    print("-" * 70)
    
    for i in range(1, min(6, len(df_googl))):
        stock_dr = df_googl.iloc[i]['daily_return']
        sp500_dr = df_googl.iloc[i]['sp500_daily_return']
        rel = df_googl.iloc[i]['relative_return']
        print(f"{i:<4} {df_googl.iloc[i]['Date'].strftime('%Y-%m-%d'):<12} "
              f"{stock_dr:<12.4f} {sp500_dr:<12.4f} {rel:<12.4f}")
    
    # ========== EXAMPLE 5: Forward Return (Label Dependency) ==========
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Forward Return Dependency (for Labels)")
    print("=" * 70)
    
    # Compute forward returns
    df_googl['stock_fwd_21d'] = df_googl['Close'].shift(-21) / df_googl['Close'] - 1
    df_googl['sp500_fwd_21d'] = df_googl['sp500_Close'].shift(-21) / df_googl['sp500_Close'] - 1
    df_googl['outperform'] = (df_googl['stock_fwd_21d'] > df_googl['sp500_fwd_21d']).astype(int)
    
    print("\nForward return depends on FUTURE Close price:")
    print("stock_fwd_21d[t] = (Close[t+21] - Close[t]) / Close[t]")
    print("⚠ WARNING: Requires future data - compute BEFORE filtering!")
    print("\n" + "-" * 70)
    print(f"{'Row':<4} {'Date':<12} {'Close[t]':<12} {'Close[t+21]':<12} {'fwd_21d':<12} {'Outperform'}")
    print("-" * 70)
    
    for i in range(min(5, len(df_googl)-21)):
        curr_close = df_googl.iloc[i]['Close']
        future_close = df_googl.iloc[i+21]['Close'] if i+21 < len(df_googl) else np.nan
        fwd = df_googl.iloc[i]['stock_fwd_21d']
        outperf = df_googl.iloc[i]['outperform']
        future_date = df_googl.iloc[i+21]['Date'].strftime('%Y-%m-%d') if i+21 < len(df_googl) else 'N/A'
        fwd_str = f"{fwd:.4f}" if not np.isnan(fwd) else "N/A"
        future_close_str = f"{future_close:.4f}" if not np.isnan(future_close) else "N/A"
        outperf_str = str(int(outperf)) if not np.isnan(outperf) else "N/A"
        print(f"{i:<4} {df_googl.iloc[i]['Date'].strftime('%Y-%m-%d'):<12} "
              f"{curr_close:<12.4f} {future_close_str:<12} "
              f"{fwd_str:<12} {outperf_str}")
        if i+21 < len(df_googl):
            print(f"      └─ Future date: {future_date}")
    
    # ========== EXAMPLE 6: Macro Data Dependency ==========
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Macro Data Dependency (CPI Change)")
    print("=" * 70)
    
    # CPI change - depends on monthly CPI values
    df_googl['CPI_change'] = df_googl['CPI'].pct_change()
    
    print("\nCPI_change depends on CPI values (monthly, forward-filled to daily):")
    print("CPI_change[t] = (CPI[t] - CPI[t-1]) / CPI[t-1]")
    print("Note: CPI is monthly data, so most days have same CPI value")
    print("\n" + "-" * 70)
    print(f"{'Row':<4} {'Date':<12} {'CPI[t-1]':<12} {'CPI[t]':<12} {'CPI_change':<12}")
    print("-" * 70)
    
    # Find rows where CPI actually changes
    cpi_changes = df_googl[df_googl['CPI_change'].notna() & (df_googl['CPI_change'] != 0)].head(5)
    for idx, row in cpi_changes.iterrows():
        prev_cpi = df_googl.iloc[idx-1]['CPI'] if idx > 0 else np.nan
        curr_cpi = row['CPI']
        cpi_chg = row['CPI_change']
        print(f"{idx:<4} {row['Date'].strftime('%Y-%m-%d'):<12} "
              f"{prev_cpi if not np.isnan(prev_cpi) else 'N/A':<12} "
              f"{curr_cpi:<12.2f} {cpi_chg:<12.6f}")
    
    print("\nNote: CPI changes occur monthly, same value forward-filled to all trading days in month")
    
    # ========== DEPENDENCY GRAPH SUMMARY ==========
    print("\n" + "=" * 70)
    print("DEPENDENCY GRAPH SUMMARY")
    print("=" * 70)
    
    print("\nRaw Data Sources → Features → Labels:")
    print("""
    Raw Columns:
      ├─ Close → daily_return → volatility_21d
      ├─ Close → rolling_return_5d, rolling_return_21d, rolling_return_63d
      ├─ Close → MA20, MA50 → ma20_ratio, ma50_ratio
      ├─ High, Low, Close → price_range
      ├─ Volume → volume_zscore
      │
      ├─ sp500_Close → sp500_daily_return → sp500_volatility
      │
      ├─ Close + sp500_Close → relative_return, volatility_ratio
      │
      ├─ Close (future) → stock_fwd_21d ┐
      ├─ sp500_Close (future) → sp500_fwd_21d ┘ → outperform_label
      │
      ├─ CPI → CPI_change
      ├─ Fed_Funds_Rate → Fed_Funds_change
      │
      └─ spy_RSI, spy_SMA_50/200 → spy_rsi_signal, spy_ma_trend
    """)
    
    print("\n" + "=" * 70)
    print("KEY INSIGHTS")
    print("=" * 70)
    print("""
    1. Most features depend on Close price (directly or indirectly)
    2. Rolling features require lookback windows (5d, 21d, 63d)
    3. Volatility depends on daily_return (2-level dependency)
    4. Relative features require computing both stock and SP500 metrics
    5. Labels require FUTURE data - compute early, filter later
    6. Macro data is monthly, forward-filled to daily
    7. Group by 'stock' when computing rolling statistics
    """)

if __name__ == '__main__':
    show_concrete_examples()

