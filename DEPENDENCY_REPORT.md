# Functional Dependencies Report

## Overview
This report documents all functional dependencies detected in the integrated dataset. Each feature's dependencies on raw data and other features are identified with examples.

---

## 1. Stock Price-Based Dependencies

### 1.1 Daily Return
- **Depends on**: `Close` (current and previous)
- **Function**: `Close.pct_change()`
- **Dependency Type**: Direct (1-level)
- **Example**: 
  - Row 1: Close = 2.4938, Previous = N/A → daily_return = NaN
  - Row 2: Close = 2.6919, Previous = 2.4938 → daily_return = 0.0794
- **Computation**: Must group by `stock` when computing

### 1.2 Rolling Returns
- **5-day rolling return**
  - Depends on: `Close` (5 days apart)
  - Function: `Close.pct_change(5)`
  - Uses: Current Close and Close from 5 days ago
  
- **21-day rolling return**
  - Depends on: `Close` (21 days apart)
  - Function: `Close.pct_change(21)`
  - Uses: Current Close and Close from 21 days ago (1 month)
  
- **63-day rolling return**
  - Depends on: `Close` (63 days apart)
  - Function: `Close.pct_change(63)`
  - Uses: Current Close and Close from 63 days ago (3 months)

### 1.3 Volatility (21-day)
- **Depends on**: `daily_return` (which depends on `Close`)
- **Function**: `daily_return.rolling(21).std()`
- **Dependency Type**: Indirect (2-level)
- **Dependency Chain**: `Close` → `daily_return` → `volatility_21d`
- **Note**: Requires 21 previous daily_return values

### 1.4 Moving Average Ratios
- **MA20 Ratio**
  - Depends on: `Close` (20 values)
  - Function: `Close / Close.rolling(20).mean()`
  - Uses: Current Close and average of last 20 Close values
  
- **MA50 Ratio**
  - Depends on: `Close` (50 values)
  - Function: `Close / Close.rolling(50).mean()`
  - Uses: Current Close and average of last 50 Close values

### 1.5 Price Range
- **Depends on**: `High`, `Low`, `Close` (same day)
- **Function**: `(High - Low) / Close`
- **Dependency Type**: Direct (1-level)
- **Note**: Uses all three OHLC components

### 1.6 Volume Z-Score
- **Depends on**: `Volume` (20 values)
- **Function**: `(Volume - Volume.rolling(20).mean()) / Volume.rolling(20).std()`
- **Dependency Type**: Direct (1-level)
- **Note**: Requires 20 previous Volume values for mean and std

---

## 2. SP500 Comparison Dependencies

### 2.1 SP500 Daily Return
- **Depends on**: `sp500_Close` (current and previous)
- **Function**: `sp500_Close.pct_change()`
- **Dependency Type**: Independent from stock features
- **Note**: Computed separately, not grouped by stock

### 2.2 Relative Return
- **Depends on**: `daily_return` AND `sp500_daily_return`
- **Function**: `daily_return - sp500_daily_return`
- **Dependency Type**: Combined (requires 2 independent chains)
- **Dependency Chain**: 
  - Chain 1: `Close` → `daily_return`
  - Chain 2: `sp500_Close` → `sp500_daily_return`
  - Then: `relative_return = stock_daily_return - sp500_daily_return`

### 2.3 SP500 Volatility
- **Depends on**: `sp500_daily_return`
- **Function**: `sp500_daily_return.rolling(21).std()`
- **Dependency Type**: Indirect (2-level)
- **Chain**: `sp500_Close` → `sp500_daily_return` → `sp500_volatility`

### 2.4 Volatility Ratio
- **Depends on**: `volatility_21d` AND `sp500_volatility`
- **Function**: `volatility_21d / sp500_volatility`
- **Dependency Type**: Combined (requires both volatilities)
- **Full Chain**: 
  - `Close` → `daily_return` → `volatility_21d`
  - `sp500_Close` → `sp500_daily_return` → `sp500_volatility`
  - Then: `volatility_ratio = volatility_21d / sp500_volatility`

---

## 3. Label Construction Dependencies

### 3.1 Stock Forward Return (21-day)
- **Depends on**: `Close` (current) AND `Close` (21 days in future)
- **Function**: `Close.shift(-21) / Close - 1`
- **Dependency Type**: Forward-looking (requires future data)
- **⚠️ Critical**: Must be computed BEFORE any data filtering
- **Example**:
  - Row 0 (2004-08-19): Close = 2.4938
  - Row 21 (2004-09-20): Close = 2.9665
  - Forward return = (2.9665 / 2.4938) - 1 = 0.1896

### 3.2 SP500 Forward Return (21-day)
- **Depends on**: `sp500_Close` (current) AND `sp500_Close` (21 days in future)
- **Function**: `sp500_Close.shift(-21) / sp500_Close - 1`
- **Dependency Type**: Forward-looking (requires future data)

### 3.3 Outperform Label
- **Depends on**: `stock_forward_return_21d` AND `sp500_forward_return_21d`
- **Function**: `(stock_fwd_ret > sp500_fwd_ret).astype(int)`
- **Dependency Type**: Combined boolean comparison
- **Values**: 1 if stock outperforms, 0 otherwise

---

## 4. Macro Data Dependencies

### 4.1 CPI Change
- **Depends on**: `CPI` (current and previous)
- **Function**: `CPI.pct_change()` or `CPI.diff()`
- **Frequency**: Monthly (forward-filled to daily)
- **Note**: Most days have same CPI value (only changes monthly)

### 4.2 CPI Year-over-Year
- **Depends on**: `CPI` (~252 trading days apart)
- **Function**: `CPI.pct_change(252)`
- **Uses**: Current CPI and CPI from ~1 year ago

### 4.3 Fed Funds Rate Change
- **Depends on**: `Fed_Funds_Rate` (current and previous)
- **Function**: `Fed_Funds_Rate.diff()`
- **Frequency**: Daily (already daily from FRED)
- **Note**: Changes occur periodically when Fed adjusts rates

### 4.4 GDP Change
- **Depends on**: `GDP` (current and previous)
- **Function**: `GDP.pct_change()` or `GDP.diff()`
- **Frequency**: Quarterly (forward-filled to daily)

---

## 5. Technical Indicator Dependencies

### 5.1 SPY RSI Signal
- **Depends on**: `spy_RSI` (already computed)
- **Function**: `1 if spy_RSI > 70 else (-1 if spy_RSI < 30 else 0)`
- **Dependency Type**: Derived signal (not computed, just categorized)
- **Meaning**: Overbought (>70), Oversold (<30), Neutral (30-70)

### 5.2 SPY MA Trend (Golden/Death Cross)
- **Depends on**: `spy_SMA_50` AND `spy_SMA_200`
- **Function**: `1 if spy_SMA_50 > spy_SMA_200 else 0`
- **Dependency Type**: Combined comparison
- **Meaning**: 1 = Bullish trend (50>200), 0 = Bearish trend

### 5.3 QQQ MA Trend
- **Depends on**: `qqq_SMA_50` AND `qqq_SMA_200`
- **Function**: `1 if qqq_SMA_50 > qqq_SMA_200 else 0`
- **Dependency Type**: Combined comparison
- **Meaning**: Tech sector trend indicator

---

## 6. Market Sentiment Dependencies

### 6.1 VIX Level
- **Depends on**: `VIX` (already available)
- **Function**: Direct use (no computation needed)
- **Meaning**: Market fear/volatility expectation

### 6.2 VIX Signal
- **Depends on**: `VIX`
- **Function**: `1 if VIX > 20 else 0`
- **Dependency Type**: Derived signal
- **Meaning**: High volatility (>20) vs Low volatility

### 6.3 Sector Relative Performance
- **Depends on**: `sector_XLK` (or other sector) AND `sp500_daily_return`
- **Function**: `sector_XLK.pct_change() - sp500_daily_return`
- **Dependency Type**: Combined
- **Meaning**: Sector performance vs market performance

---

## 7. Dependency Graph Summary

```
Raw Data Sources:
│
├─ Stock OHLCV
│  ├─ Close
│  │  ├─ → daily_return
│  │  │  └─ → volatility_21d
│  │  ├─ → rolling_return_5d, 21d, 63d
│  │  ├─ → MA20, MA50 → ma20_ratio, ma50_ratio
│  │  └─ → stock_fwd_21d (future)
│  ├─ High, Low, Close → price_range
│  └─ Volume → volume_zscore
│
├─ SP500 OHLCV
│  ├─ sp500_Close
│  │  ├─ → sp500_daily_return → sp500_volatility
│  │  └─ → sp500_fwd_21d (future)
│  │
│  └─ Combined with stock:
│     ├─ daily_return + sp500_daily_return → relative_return
│     └─ volatility_21d + sp500_volatility → volatility_ratio
│
├─ Macro Data
│  ├─ CPI → CPI_change, CPI_yoy
│  ├─ Fed_Funds_Rate → Fed_Funds_change
│  └─ GDP → GDP_change
│
├─ Market Indicators
│  ├─ VIX → vix_signal
│  ├─ sector_XLK → sector_relative_performance
│  └─ Put_Call_Ratio, Market_Breadth (direct use)
│
└─ Technical Indicators
   ├─ spy_RSI → spy_rsi_signal
   ├─ spy_SMA_50, spy_SMA_200 → spy_ma_trend
   └─ qqq_SMA_50, qqq_SMA_200 → qqq_ma_trend
│
└─ Labels
   └─ stock_fwd_21d + sp500_fwd_21d → outperform_label
```

---

## 8. Critical Dependencies & Warnings

### 8.1 Forward-Looking Features
- **Features**: `stock_fwd_21d`, `sp500_fwd_21d`, `outperform_label`
- **Warning**: Require future data (21 days ahead)
- **Action**: Compute BEFORE any data filtering or train/test split
- **Impact**: Last 21 rows of each stock will have NaN forward returns

### 8.2 Rolling Window Requirements
- **Features**: `volatility_21d`, `ma20_ratio`, `ma50_ratio`, `volume_zscore`
- **Warning**: Require N previous rows (N = window size)
- **Action**: First N rows will have NaN values
- **Example**: `ma20_ratio` first available at row 20 (uses rows 1-20)

### 8.3 Grouping Requirements
- **Features**: All stock-specific features
- **Warning**: Must group by `stock` when computing
- **Action**: Use `df.groupby('stock')` before rolling operations
- **Example**: `df.groupby('stock')['Close'].pct_change()`

### 8.4 Macro Data Frequency
- **Features**: `CPI_change`, `GDP_change`
- **Warning**: Monthly/quarterly data forward-filled to daily
- **Action**: Most days have same value, changes occur periodically
- **Note**: Use `pct_change()` or `diff()` to detect actual changes

---

## 9. Recommended Computation Order

1. **Base stock features** (daily_return, price_range)
2. **Rolling stock features** (rolling returns, volatility, MA ratios, volume_zscore)
3. **SP500 features** (sp500_daily_return, sp500_volatility)
4. **Relative features** (relative_return, volatility_ratio)
5. **Forward returns** (stock_fwd_21d, sp500_fwd_21d) ⚠️ BEFORE filtering
6. **Labels** (outperform_label)
7. **Macro derivatives** (CPI_change, Fed_Funds_change, GDP_change)
8. **Technical signals** (if needed: RSI signals, MA trends)
9. **Market sentiment signals** (if needed: VIX signal, sector relative)

---

## 10. Dependency Examples

See `dependency_examples.py` for concrete examples with actual data values demonstrating:
- Daily return calculations
- MA ratio computations
- Volatility dependency chains
- Relative return comparisons
- Forward return calculations
- Macro data dependencies

---

**Report Generated**: Based on analysis of integrated_raw_data.csv
**Total Features Identified**: 20+ feature dependencies
**Dependency Levels**: 1-level (direct) to 3-level (indirect chains)

