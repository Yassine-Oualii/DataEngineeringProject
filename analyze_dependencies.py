"""
Analyze Function Dependencies in Integrated Dataset

Detects and documents how different features depend on each other
and on the raw data columns.
"""

import pandas as pd
import numpy as np

def analyze_dependencies():
    """
    Analyze dependencies in the integrated dataset and show examples.
    """
    print("=" * 70)
    print("DEPENDENCY ANALYSIS - Integrated Dataset")
    print("=" * 70)
    
    # Load integrated data
    df = pd.read_csv('data/integrated_raw_data.csv', nrows=100)  # Sample for analysis
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index(['stock', 'Date']).sort_index()
    
    print(f"\nDataset shape: {df.shape}")
    print(f"Columns: {len(df.columns)}")
    print(f"\nAvailable raw columns:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i:2d}. {col}")
    
    # ========== DEPENDENCY CATEGORIES ==========
    
    print("\n" + "=" * 70)
    print("DEPENDENCY CATEGORIES")
    print("=" * 70)
    
    # 1. STOCK PRICE DEPENDENCIES
    print("\n1. STOCK PRICE-BASED DEPENDENCIES")
    print("-" * 70)
    
    stock_deps = {
        "daily_return": {
            "depends_on": ["Close"],
            "function": "Close.pct_change()",
            "description": "Daily return depends on current and previous Close price",
            "example": "df['daily_return'] = df.groupby('stock')['Close'].pct_change()"
        },
        "rolling_return_5d": {
            "depends_on": ["Close"],
            "function": "Close.pct_change(5)",
            "description": "5-day rolling return depends on Close prices 5 days apart",
            "example": "df['rolling_ret_5d'] = df.groupby('stock')['Close'].pct_change(5)"
        },
        "rolling_return_21d": {
            "depends_on": ["Close"],
            "function": "Close.pct_change(21)",
            "description": "21-day rolling return (1 month) depends on Close prices 21 days apart",
            "example": "df['rolling_ret_21d'] = df.groupby('stock')['Close'].pct_change(21)"
        },
        "rolling_return_63d": {
            "depends_on": ["Close"],
            "function": "Close.pct_change(63)",
            "description": "63-day rolling return (3 months) depends on Close prices 63 days apart",
            "example": "df['rolling_ret_63d'] = df.groupby('stock')['Close'].pct_change(63)"
        },
        "volatility_21d": {
            "depends_on": ["daily_return"],
            "function": "daily_return.rolling(21).std()",
            "description": "21-day volatility depends on daily_return (which depends on Close)",
            "example": "df['volatility_21d'] = df.groupby('stock')['daily_return'].rolling(21).std()"
        },
        "ma20_ratio": {
            "depends_on": ["Close"],
            "function": "Close / Close.rolling(20).mean()",
            "description": "Price to 20-day MA ratio depends on Close and its 20-day moving average",
            "example": "df['ma20_ratio'] = df.groupby('stock')['Close'] / df.groupby('stock')['Close'].rolling(20).mean()"
        },
        "ma50_ratio": {
            "depends_on": ["Close"],
            "function": "Close / Close.rolling(50).mean()",
            "description": "Price to 50-day MA ratio depends on Close and its 50-day moving average",
            "example": "df['ma50_ratio'] = df.groupby('stock')['Close'] / df.groupby('stock')['Close'].rolling(50).mean()"
        },
        "price_range": {
            "depends_on": ["High", "Low", "Close"],
            "function": "(High - Low) / Close",
            "description": "Price range depends on High, Low, and Close of same day",
            "example": "df['price_range'] = (df['High'] - df['Low']) / df['Close']"
        },
        "volume_zscore": {
            "depends_on": ["Volume"],
            "function": "(Volume - Volume.rolling(20).mean()) / Volume.rolling(20).std()",
            "description": "Volume z-score depends on Volume and its 20-day rolling statistics",
            "example": "df['volume_zscore'] = (df['Volume'] - df.groupby('stock')['Volume'].rolling(20).mean()) / df.groupby('stock')['Volume'].rolling(20).std()"
        }
    }
    
    for feature, deps in stock_deps.items():
        print(f"\n  {feature}:")
        print(f"    Depends on: {', '.join(deps['depends_on'])}")
        print(f"    Function: {deps['function']}")
        print(f"    {deps['description']}")
    
    # 2. SP500 COMPARISON DEPENDENCIES
    print("\n\n2. SP500 COMPARISON DEPENDENCIES")
    print("-" * 70)
    
    sp500_deps = {
        "sp500_daily_return": {
            "depends_on": ["sp500_Close"],
            "function": "sp500_Close.pct_change()",
            "description": "SP500 daily return depends on sp500_Close"
        },
        "relative_return": {
            "depends_on": ["daily_return", "sp500_daily_return"],
            "function": "daily_return - sp500_daily_return",
            "description": "Relative return compares stock return to SP500 return",
            "example": "df['relative_return'] = df['daily_return'] - df['sp500_daily_return']"
        },
        "sp500_volatility": {
            "depends_on": ["sp500_daily_return"],
            "function": "sp500_daily_return.rolling(21).std()",
            "description": "SP500 volatility depends on its daily returns"
        },
        "volatility_ratio": {
            "depends_on": ["volatility_21d", "sp500_volatility"],
            "function": "volatility_21d / sp500_volatility",
            "description": "Ratio comparing stock volatility to market volatility"
        }
    }
    
    for feature, deps in sp500_deps.items():
        print(f"\n  {feature}:")
        print(f"    Depends on: {', '.join(deps['depends_on'])}")
        print(f"    Function: {deps['function']}")
        print(f"    {deps['description']}")
    
    # 3. LABEL DEPENDENCIES
    print("\n\n3. LABEL CONSTRUCTION DEPENDENCIES")
    print("-" * 70)
    
    label_deps = {
        "stock_forward_return_21d": {
            "depends_on": ["Close"],
            "function": "Close.shift(-21) / Close - 1",
            "description": "Forward 21-day return depends on current Close and Close 21 days ahead",
            "note": "Must be computed BEFORE removing future data"
        },
        "sp500_forward_return_21d": {
            "depends_on": ["sp500_Close"],
            "function": "sp500_Close.shift(-21) / sp500_Close - 1",
            "description": "SP500 forward return depends on current sp500_Close and Close 21 days ahead"
        },
        "outperform_label": {
            "depends_on": ["stock_forward_return_21d", "sp500_forward_return_21d"],
            "function": "(stock_fwd_ret > sp500_fwd_ret).astype(int)",
            "description": "Binary label: 1 if stock outperforms SP500, 0 otherwise"
        }
    }
    
    for feature, deps in label_deps.items():
        print(f"\n  {feature}:")
        print(f"    Depends on: {', '.join(deps['depends_on'])}")
        print(f"    Function: {deps['function']}")
        print(f"    {deps['description']}")
        if 'note' in deps:
            print(f"    ⚠ Note: {deps['note']}")
    
    # 4. MACRO DATA DEPENDENCIES
    print("\n\n4. MACRO DATA DEPENDENCIES")
    print("-" * 70)
    
    macro_deps = {
        "CPI_change": {
            "depends_on": ["CPI"],
            "function": "CPI.pct_change() or CPI.diff()",
            "description": "CPI change depends on CPI values over time",
            "frequency": "Monthly macro data forward-filled to daily"
        },
        "CPI_yoy": {
            "depends_on": ["CPI"],
            "function": "CPI.pct_change(252)  # ~1 year trading days",
            "description": "Year-over-year CPI change"
        },
        "Fed_Funds_change": {
            "depends_on": ["Fed_Funds_Rate"],
            "function": "Fed_Funds_Rate.diff()",
            "description": "Fed Funds rate change (already daily from FRED)"
        }
    }
    
    for feature, deps in macro_deps.items():
        print(f"\n  {feature}:")
        print(f"    Depends on: {', '.join(deps['depends_on'])}")
        print(f"    Function: {deps['function']}")
        print(f"    {deps['description']}")
        if 'frequency' in deps:
            print(f"    Frequency: {deps['frequency']}")
    
    # 5. TECHNICAL INDICATOR DEPENDENCIES
    print("\n\n5. TECHNICAL INDICATOR DEPENDENCIES")
    print("-" * 70)
    
    tech_deps = {
        "spy_rsi_signal": {
            "depends_on": ["spy_RSI"],
            "function": "1 if spy_RSI > 70 else (-1 if spy_RSI < 30 else 0)",
            "description": "RSI overbought/oversold signal (already computed, but can derive signals)"
        },
        "spy_ma_trend": {
            "depends_on": ["spy_SMA_50", "spy_SMA_200"],
            "function": "1 if spy_SMA_50 > spy_SMA_200 else 0",
            "description": "Golden/Death cross indicator - market trend signal"
        },
        "qqq_ma_trend": {
            "depends_on": ["qqq_SMA_50", "qqq_SMA_200"],
            "function": "1 if qqq_SMA_50 > qqq_SMA_200 else 0",
            "description": "QQQ trend indicator - tech sector trend"
        }
    }
    
    for feature, deps in tech_deps.items():
        print(f"\n  {feature}:")
        print(f"    Depends on: {', '.join(deps['depends_on'])}")
        print(f"    Function: {deps['function']}")
        print(f"    {deps['description']}")
    
    # 6. MARKET SENTIMENT DEPENDENCIES
    print("\n\n6. MARKET SENTIMENT DEPENDENCIES")
    print("-" * 70)
    
    sentiment_deps = {
        "vix_level": {
            "depends_on": ["VIX"],
            "function": "VIX (already available)",
            "description": "VIX level indicates market fear/volatility expectation"
        },
        "vix_signal": {
            "depends_on": ["VIX"],
            "function": "1 if VIX > 20 else 0  # High volatility signal",
            "description": "Derived signal from VIX level"
        },
        "sector_relative_performance": {
            "depends_on": ["sector_XLK", "sp500_Close"],
            "function": "sector_XLK.pct_change() - sp500_daily_return",
            "description": "Sector performance relative to market"
        }
    }
    
    for feature, deps in sentiment_deps.items():
        print(f"\n  {feature}:")
        print(f"    Depends on: {', '.join(deps['depends_on'])}")
        print(f"    Function: {deps['function']}")
        print(f"    {deps['description']}")
    
    # ========== DEPENDENCY GRAPH EXAMPLES ==========
    
    print("\n" + "=" * 70)
    print("DEPENDENCY CHAIN EXAMPLES")
    print("=" * 70)
    
    examples = [
        {
            "target": "outperform_label",
            "chain": [
                "Close → daily_return",
                "daily_return → volatility_21d",
                "Close → stock_forward_return_21d",
                "sp500_Close → sp500_forward_return_21d",
                "stock_forward_return_21d + sp500_forward_return_21d → outperform_label"
            ],
            "description": "Label depends on forward returns, which depend on Close prices"
        },
        {
            "target": "ma20_ratio",
            "chain": [
                "Close → Close.rolling(20).mean() (MA20)",
                "Close + MA20 → ma20_ratio"
            ],
            "description": "MA ratio requires computing moving average first"
        },
        {
            "target": "volatility_ratio",
            "chain": [
                "Close → daily_return",
                "daily_return → volatility_21d",
                "sp500_Close → sp500_daily_return",
                "sp500_daily_return → sp500_volatility",
                "volatility_21d + sp500_volatility → volatility_ratio"
            ],
            "description": "Relative volatility requires computing both stock and market volatility"
        }
    ]
    
    for i, ex in enumerate(examples, 1):
        print(f"\n{i}. Target Feature: {ex['target']}")
        print(f"   Description: {ex['description']}")
        print(f"   Dependency Chain:")
        for step in ex['chain']:
            print(f"     {step}")
    
    # ========== COMPUTATION ORDER RECOMMENDATIONS ==========
    
    print("\n" + "=" * 70)
    print("RECOMMENDED COMPUTATION ORDER")
    print("=" * 70)
    
    order = [
        "1. Base price features (daily_return, price_range)",
        "2. Rolling statistics (rolling returns, volatility, MA)",
        "3. SP500 features (sp500_daily_return, sp500_volatility)",
        "4. Relative features (relative_return, volatility_ratio)",
        "5. Forward returns (for labels - BEFORE any filtering)",
        "6. Labels (outperform_label)",
        "7. Macro derivatives (CPI_change, Fed change)",
        "8. Technical indicator signals (if needed)",
        "9. Market sentiment signals (if needed)"
    ]
    
    for step in order:
        print(f"   {step}")
    
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)

if __name__ == '__main__':
    analyze_dependencies()

