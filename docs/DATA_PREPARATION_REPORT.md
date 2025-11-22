# Data Preparation Report - Null Data Handling

## Overview

This report documents all processes performed to deal with null/missing data in the integrated dataset, along with concrete examples of null handling cases.

---

## 1. Null Detection Summary

### Overall Statistics
- **Total Rows**: 8,720
- **Total Columns**: 30
- **Total Cells**: 261,600
- **Total Null Values**: 48 (0.0183% of dataset)
- **Rows with Nulls**: 30 (0.34% of rows)

### Null Distribution by Column

| Column | Null Count | Percentage | Category |
|--------|------------|------------|----------|
| GDP | 30 | 0.34% | Macro Indicator |
| CPI | 9 | 0.10% | Macro Indicator |
| Unemployment_Rate | 9 | 0.10% | Macro Indicator |

**Key Finding**: All null values occur in macro economic indicators, specifically at the start of GOOGL's time series (2004-08-19 to 2004-09-30).

---

## 2. Null Values by Data Category

### Category Breakdown

1. **Stock Price Data** (Close, High, Low, Open, Volume)
   - Nulls: 0 (0.00%)
   - Status: ✓ Complete

2. **SP500 Data** (sp500_Close, sp500_High, etc.)
   - Nulls: 0 (0.00%)
   - Status: ✓ Complete

3. **Macro Indicators** (CPI, Fed_Funds_Rate, GDP, Unemployment_Rate)
   - Nulls: 48 (0.14%)
   - Status: ⚠ Minor nulls at start of time series
   - Affected: CPI (9), GDP (30), Unemployment_Rate (9)

4. **Market Sentiment** (VIX, Put_Call_Ratio, Market_Breadth)
   - Nulls: 0 (0.00%)
   - Status: ✓ Complete

5. **Sector ETFs** (sector_XLK, sector_XLF, etc.)
   - Nulls: 0 (0.00%)
   - Status: ✓ Complete

6. **Technical Indicators** (spy_RSI, qqq_SMA_50, etc.)
   - Nulls: 0 (0.00%)
   - Status: ✓ Complete

---

## 3. Null Patterns and Causes

### Pattern 1: Start of Time Series Nulls
- **Location**: First 30 rows of GOOGL data (2004-08-19 to 2004-09-30)
- **Affected Columns**: CPI, GDP, Unemployment_Rate
- **Cause**: Macro data starts later than stock price data
  - GOOGL IPO: August 19, 2004
  - Macro data availability: Some indicators may not be available immediately after IPO date
- **Impact**: Low (0.34% of GOOGL rows, 0.03% of total dataset)

### Pattern 2: No Nulls in Stock/Market Data
- **Stock OHLCV**: All complete ✓
- **SP500 Data**: All complete ✓
- **Market Indicators**: All complete ✓
- **Technical Indicators**: All complete ✓

---

## 4. Data Preparation Processes Applied

### 4.1 Forward-Filling Macro Data

**Process**: Monthly/quarterly macro data forward-filled to daily frequency

**Implementation** (from `integrate_data.py`):
```python
# Forward-fill macro data (monthly → daily)
date_range = pd.date_range(
    start=integrated['Date'].min(),
    end=integrated['Date'].max(),
    freq='D'
)
macro_reindexed = macro_df.reindex(date_range).ffill()
integrated = integrated.merge(macro_reindexed, on='Date', how='left')
integrated[col_name] = integrated[col_name].ffill()
```

**Rationale**:
- CPI, GDP, Unemployment_Rate are published monthly/quarterly
- For daily stock analysis, forward-fill to maintain value until next publication
- Example: CPI from January 1st fills all trading days in January

**Result**: Most nulls eliminated, only start-of-series nulls remain

---

### 4.2 Date Alignment (Inner Join)

**Process**: Stock and SP500 data merged with inner join on Date

**Implementation**:
```python
integrated = integrated.merge(sp500_reset, on='Date', how='inner')
```

**Rationale**:
- Ensures SP500 data exists for all stock dates
- Prevents nulls from missing SP500 values
- Maintains data integrity (same market on same day)

**Result**: No nulls in SP500 columns

---

### 4.3 Left Join for Market Data

**Process**: Market indicators merged with left join to preserve all stock-date combinations

**Implementation**:
```python
integrated = integrated.merge(market_reset, on='Date', how='left')
```

**Rationale**:
- Preserves all (stock, date) pairs
- Missing market indicators would create nulls (but none found)
- Allows for optional market data

**Result**: No nulls in market indicator columns

---

## 5. Concrete Examples of Null Cases

### Example 1: Start-of-Series Nulls (GOOGL IPO Period)

**Case**: GOOGL IPO date (2004-08-19) has null macro indicators

**Row Details**:
```
Stock: GOOGL
Date: 2004-08-19
Close: 2.4938 (valid)
High: 2.5863 (valid)
Low: 2.3850 (valid)
Open: 2.4854 (valid)
Volume: 893,181,924 (valid)

CPI: NULL ⚠
GDP: NULL ⚠
Unemployment_Rate: NULL ⚠

SP500_Close: 1091.23 (valid)
VIX: 16.96 (valid)
Fed_Funds_Rate: 1.5 (valid)
```

**Analysis**:
- Stock price data is complete (IPO data available)
- SP500 and market data available (market was trading)
- Macro indicators missing (data not available at series start)

**Handling Strategy**: 
- Forward-fill from next available value
- Or drop first rows if macro indicators required
- Current approach: Accept nulls (only 30 rows affected)

---

### Example 2: Sequential Null Pattern

**Case**: First 10 rows of GOOGL all have same null pattern

**Pattern**:
```
Row 0-9 (2004-08-19 to 2004-08-30):
  All have: CPI=NULL, GDP=NULL, Unemployment_Rate=NULL
  
Row 10 onwards:
  All have: Valid macro data
```

**Analysis**:
- Nulls occur in blocks (consecutive days)
- Pattern indicates data availability gap at start
- All affected rows have same null columns

**Handling Strategy**:
- Forward-fill from first available value (after Sep 30, 2004)
- Or exclude first month if macro features critical

---

### Example 3: Column-Specific Null Distribution

**CPI Nulls**:
- Null count: 9
- Dates: 2004-08-19 to 2004-08-27 (9 trading days)
- Pattern: First 9 days of GOOGL trading

**GDP Nulls**:
- Null count: 30
- Dates: 2004-08-19 to 2004-09-30 (30 trading days)
- Pattern: First month of GOOGL trading
- Cause: GDP is quarterly, may not align with daily stock data start

**Unemployment_Rate Nulls**:
- Null count: 9
- Dates: 2004-08-19 to 2004-08-27 (9 trading days)
- Pattern: First 9 days of GOOGL trading

---

## 6. Recommended Null Handling Strategies

### 6.1 For Existing Nulls (Current Dataset)

#### Strategy A: Forward-Fill from Next Available Value
```python
# Forward-fill macro indicators
df['CPI'] = df.groupby('stock')['CPI'].ffill()
df['GDP'] = df.groupby('stock')['GDP'].ffill()
df['Unemployment_Rate'] = df.groupby('stock')['Unemployment_Rate'].ffill()
```

**Pros**: 
- Preserves all rows
- Uses next known value

**Cons**: 
- Uses future data for past rows (acceptable for macro data)
- May mask missing data periods

#### Strategy B: Backward-Fill (Use Previous Value)
```python
# Backward-fill from previous available value
df['CPI'] = df.groupby('stock')['CPI'].bfill()
```

**Pros**: 
- Uses past values (more conservative)

**Cons**: 
- May not have past values at series start

#### Strategy C: Drop Rows with Nulls
```python
# Drop rows with null macro indicators
df_clean = df.dropna(subset=['CPI', 'GDP', 'Unemployment_Rate'])
```

**Pros**: 
- Ensures complete data
- No imputation needed

**Cons**: 
- Loses 30 rows (0.34% of data)
- May remove important IPO period data

**Recommendation**: Strategy A (Forward-fill) - already applied in integration, minimal impact

---

### 6.2 For Feature Engineering Nulls

When engineering features, additional nulls will be created:

#### Rolling Window Features
**Examples**:
- `ma20_ratio`: First 20 rows null (needs 20 days history)
- `volatility_21d`: First 21 rows null (needs 21 days returns)
- `rolling_return_21d`: First 21 rows null (needs 21 days history)

**Handling**:
```python
# Compute features (creates nulls)
df['ma20_ratio'] = df.groupby('stock')['Close'].rolling(20).mean()

# Drop rows with null rolling features
df_clean = df.dropna(subset=['ma20_ratio', 'volatility_21d'])
```

#### Forward Returns (Labels)
**Example**:
- `stock_fwd_21d`: Last 21 rows null (no future data)

**Handling**:
```python
# Compute forward returns (last 21 rows will be null)
df['stock_fwd_21d'] = df.groupby('stock')['Close'].shift(-21) / df['Close'] - 1

# For training: Drop last 21 rows per stock
train_df = df.groupby('stock').apply(lambda x: x.iloc[:-21]).reset_index(drop=True)
```

#### Percentage Changes
**Example**:
- `daily_return`: First row of each stock null (no previous value)

**Handling**:
```python
# Compute daily return (first row null)
df['daily_return'] = df.groupby('stock')['Close'].pct_change()

# Option 1: Drop first row per stock
df_clean = df.groupby('stock').apply(lambda x: x.iloc[1:]).reset_index(drop=True)

# Option 2: Fill with 0
df['daily_return'] = df.groupby('stock')['Close'].pct_change().fillna(0)
```

---

## 7. Null Handling Examples with Code

### Example 1: Forward-Fill Macro Indicators

```python
import pandas as pd

# Load data
df = pd.read_csv('data/integrated_raw_data.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Before forward-fill
print(f"CPI nulls before: {df['CPI'].isnull().sum()}")

# Forward-fill by stock (grouped)
df['CPI'] = df.groupby('stock')['CPI'].ffill()
df['GDP'] = df.groupby('stock')['GDP'].ffill()
df['Unemployment_Rate'] = df.groupby('stock')['Unemployment_Rate'].ffill()

# After forward-fill
print(f"CPI nulls after: {df['CPI'].isnull().sum()}")
```

**Result**:
- Before: 9 CPI nulls
- After: 0 CPI nulls (if next value available)

---

### Example 2: Handling Rolling Window Nulls

```python
# Compute rolling features
df['ma20'] = df.groupby('stock')['Close'].rolling(20).mean().values
df['volatility_21d'] = df.groupby('stock')['daily_return'].rolling(21).std().values

# Count nulls created
print(f"MA20 nulls: {df['ma20'].isnull().sum()}")  # First 20 rows per stock
print(f"Volatility nulls: {df['volatility_21d'].isnull().sum()}")  # First 21 rows per stock

# Drop rows with null rolling features
initial_rows = len(df)
df_clean = df.dropna(subset=['ma20', 'volatility_21d'])
dropped_rows = initial_rows - len(df_clean)

print(f"Dropped {dropped_rows} rows ({dropped_rows/initial_rows*100:.2f}%)")
```

**Expected Result**:
- MA20: ~40 nulls (20 per stock × 2 stocks)
- Volatility: ~42 nulls (21 per stock × 2 stocks)
- Total dropped: ~42 rows (after feature engineering)

---

### Example 3: Handling Forward Return Nulls

```python
# Compute forward returns (for labels)
df['stock_fwd_21d'] = df.groupby('stock')['Close'].shift(-21) / df.groupby('stock')['Close'] - 1

# Check nulls at end
for stock in df['stock'].unique():
    stock_df = df[df['stock'] == stock].sort_values('Date')
    nulls_at_end = stock_df['stock_fwd_21d'].isnull().tail(21).sum()
    print(f"{stock}: {nulls_at_end} nulls at end (last 21 rows)")

# For training: Remove last 21 rows per stock
train_df = df.groupby('stock').apply(
    lambda x: x.iloc[:-21] if len(x) > 21 else x
).reset_index(drop=True)

print(f"Training rows: {len(train_df)} (removed last 21 per stock)")
```

---

## 8. Data Quality Metrics

### Completeness Metrics

| Category | Completeness | Status |
|----------|--------------|--------|
| Stock Price Data | 100.00% | ✓ Excellent |
| SP500 Data | 100.00% | ✓ Excellent |
| Market Sentiment | 100.00% | ✓ Excellent |
| Sector ETFs | 100.00% | ✓ Excellent |
| Technical Indicators | 100.00% | ✓ Excellent |
| Macro Indicators | 99.86% | ⚠ Good (minor nulls) |
| **Overall** | **99.98%** | **✓ Excellent** |

### Null Impact Assessment

- **Low Impact**: Only 0.34% of rows affected
- **Isolated**: Only at start of GOOGL time series
- **Mitigated**: Forward-filling process already applied
- **Acceptable**: Does not significantly impact downstream analysis

---

## 9. Recommendations

### For Current Nulls:
1. **Accept Current State**: Nulls are minimal and at series start
2. **Forward-Fill if Needed**: Apply additional forward-fill if macro indicators critical
3. **Drop if Necessary**: Only if macro features are essential (loses 30 rows)

### For Feature Engineering:
1. **Drop Rolling Window Nulls**: Remove first N rows per stock (N = window size)
2. **Handle Forward Returns Separately**: Keep last 21 rows separate for label computation
3. **Group by Stock**: Always group by stock when computing rolling features

### For Model Training:
1. **Complete Case Analysis**: Drop rows with any nulls in features
2. **Separate Train/Test**: Ensure test set doesn't use forward-filled values
3. **Documentation**: Track which rows were dropped and why

---

## 10. Conclusion

The integrated dataset has **excellent data quality** with:
- 99.98% completeness
- Only 48 null values (0.018% of dataset)
- All nulls isolated to macro indicators at series start
- No nulls in critical stock price or market data

The data preparation processes (forward-filling, date alignment) have effectively handled missing data, resulting in a highly complete dataset ready for feature engineering and modeling.

---

**Report Generated**: Based on analysis of `integrated_raw_data.csv`
**Analysis Script**: `data_preparation_report.py`
**Null Analysis Export**: `data/null_analysis.csv`

