# Outlier Detection Report

## Overview

This report documents outlier detection performed on the integrated prepared dataset using multiple statistical methods. Outliers represent extreme values that deviate significantly from the normal distribution of the data.

---

## Detection Methods

### 1. Z-Score Method
- **Threshold**: 3 standard deviations
- **Formula**: |(x - mean) / std| > 3
- **Interpretation**: Values more than 3 standard deviations from the mean
- **Characteristics**: Sensitive to extreme values, good for normally distributed data

### 2. IQR Method (Interquartile Range)
- **Threshold**: 1.5 × IQR
- **Formula**: Value < Q1 - 1.5×IQR OR Value > Q3 + 1.5×IQR
- **Interpretation**: Values beyond 1.5 times the interquartile range
- **Characteristics**: More robust to extremes, good for skewed distributions

---

## Detection Results Summary

### Z-Score Method Results
- **Columns with outliers**: 12
- **Total outlier instances**: 1,889
- **Percentage of dataset**: 0.77%

### IQR Method Results
- **Columns with outliers**: 13
- **Total outlier instances**: 5,477
- **Percentage of dataset**: 2.24%

**Note**: IQR method is more sensitive and detects more outliers (5,477 vs 1,889)

---

## Columns with Outliers

### Z-Score Method (Top Outliers)

| Column | Outliers | Percentage | Max Z-Score | Interpretation |
|--------|----------|------------|-------------|----------------|
| High | 273 | 3.13% | 4.79 | Extreme high prices |
| Close | 271 | 3.11% | 4.81 | Extreme closing prices |
| Open | 271 | 3.11% | 4.82 | Extreme opening prices |
| Low | 268 | 3.07% | 4.82 | Extreme low prices |
| Volume | 190 | 2.18% | 12.86 | Extreme trading volume |
| VIX | 174 | 2.00% | 8.06 | Market stress periods |
| Put_Call_Ratio | 174 | 2.00% | 8.06 | Extreme market sentiment |

---

## Concrete Outlier Examples

### Example 1: Volume Outliers (Extreme Trading Activity)

**Context**: Days with unusually high trading volume, often during:
- Initial Public Offerings (IPOs)
- Earnings announcements
- Major news events
- Market crashes/rallies

**Top 5 Volume Outliers:**

| Date | Stock | Volume | Z-Score | Close Price | Context |
|------|-------|--------|---------|-------------|---------|
| 2004-08-19 | GOOGL | 893,181,924 | 6.69 | $2.49 | IPO Day |
| 2004-09-29 | GOOGL | 610,329,060 | 4.36 | $3.26 | High activity |
| 2004-10-21 | GOOGL | 582,996,420 | 4.14 | $3.71 | High activity |
| 2004-08-20 | GOOGL | 456,686,856 | 3.10 | $2.69 | Post-IPO |
| 2004-10-20 | GOOGL | 454,453,092 | 3.08 | $3.49 | High activity |

**Interpretation**:
- GOOGL IPO date (2004-08-19) had volume 6.69 standard deviations above mean
- This is expected for IPO days (high initial trading interest)
- These are VALID outliers (not errors, but extreme events)

---

### Example 2: Close Price Outliers (Extreme Stock Prices)

**Context**: Highest closing prices, typically recent dates as stock prices have grown over time

**Top 5 Highest Close Prices:**

| Date | Stock | Close Price | Z-Score | Volume | Context |
|------|-------|-------------|---------|--------|---------|
| 2024-09-23 | META | $562.64 | 3.19 | 12,830,700 | Recent high |
| 2024-09-20 | META | $559.59 | 3.17 | 22,066,800 | Recent high |
| 2024-09-19 | META | $557.35 | 3.15 | 15,647,000 | Recent high |
| 2024-07-05 | META | $537.70 | 3.01 | 21,354,100 | Recent high |
| 2024-09-18 | META | $536.26 | 3.00 | 10,323,500 | Recent high |

**Interpretation**:
- All outliers are from 2024-2025 (recent dates)
- META stock has reached very high prices
- These reflect actual market values (not errors)
- Expected due to stock price growth over 20+ years

---

### Example 3: VIX Outliers (Market Stress/Fear Periods)

**Context**: VIX (Volatility Index) measures market fear. High VIX (>30) indicates extreme market stress.

**Top 5 VIX Outliers:**

| Date | VIX | Z-Score | Stock | Close Price | Historical Context |
|------|-----|---------|------|-------------|-------------------|
| 2008-10-07 | 53.68 | 4.42 | GOOGL | $8.60 | **Financial Crisis** |
| 2008-10-06 | 52.05 | 4.21 | GOOGL | $9.23 | **Financial Crisis** |
| 2008-09-29 | 46.72 | 3.54 | GOOGL | $9.47 | **Financial Crisis** |
| 2008-10-02 | 45.26 | 3.36 | GOOGL | $9.71 | **Financial Crisis** |
| 2008-10-03 | 45.14 | 3.34 | GOOGL | $9.62 | **Financial Crisis** |

**Interpretation**:
- All top outliers from October 2008 (Financial Crisis peak)
- VIX values >40 indicate extreme market panic
- These are HISTORICALLY SIGNIFICANT outliers
- Reflect real market conditions during crisis

**Why these matter**:
- During financial crisis, markets experienced extreme volatility
- VIX spiked to unprecedented levels
- These outliers capture critical market stress periods
- Important for model to learn crisis patterns

---

### Example 4: Rows with Multiple Outliers

**Context**: Some dates have multiple columns with outliers simultaneously, indicating extreme market events.

**Top 3 Rows with Most Outlier Columns:**

| Date | Stock | Outlier Count | Outlier Columns |
|------|-------|---------------|-----------------|
| 2025-04-08 | META | 6 | High, Open, sp500_Volume, ... |
| 2024-09-20 | META | 5 | Close, High, Low, ... |
| 2024-12-20 | META | 5 | Close, High, Low, ... |

**Interpretation**:
- When multiple columns are outliers simultaneously, indicates systemic market events
- Could be: market crashes, rallies, earnings announcements, major news
- These dates are particularly important for understanding extreme market behavior

---

## Method Comparison: Z-Score vs IQR

### Example: Volume Column

**Z-Score Method**:
- Outliers: 190 (2.18% of data)
- More conservative
- Only catches extreme values (>3 std devs)
- Mean-based, sensitive to the extreme values themselves

**IQR Method**:
- Outliers: 1,024 (11.74% of data)
- More sensitive
- Catches values beyond 1.5×IQR from quartiles
- Quartile-based, more robust to extremes

**Why Different?**
- Volume data is highly skewed (few very high values, many moderate values)
- IQR method catches more "moderately extreme" values
- Z-Score only catches "very extreme" values
- Both are valid, serve different purposes

---

## Outlier Analysis by Category

### Stock Price Features
- **Close, High, Low, Open**: All have ~3% outliers
- **Pattern**: Outliers mainly from:
  - Recent dates (very high prices)
  - Early dates (very low prices during IPO)
- **Interpretation**: Reflects stock price growth over time

### Volume Features
- **Volume**: 190 outliers (2.18%)
- **sp500_Volume**: 135 outliers (1.55%)
- **Pattern**: Extreme trading days (IPOs, news events, crashes)
- **Max Z-Score**: 12.86 (Volume) - very extreme!

### Market Sentiment
- **VIX**: 174 outliers (2.00%)
- **Put_Call_Ratio**: 174 outliers (2.00%)
- **Pattern**: Crisis periods (2008, 2020)
- **Interpretation**: Captures market stress events

---

## Outlier Handling Recommendations

### Option 1: Keep Outliers (Recommended)
**Reasoning**:
- Most outliers represent REAL market events
- Financial crises, IPOs, earnings - all valid extreme values
- Model should learn from these patterns
- Removing outliers would lose critical information

### Option 2: Winsorization (Cap Outliers)
**Method**: Cap extreme values at 99th/1st percentile
**When**: If outliers are causing model issues
**Risk**: May lose important crisis/event signals

### Option 3: Robust Scaling (Already Applied)
**Method**: Use RobustScaler (median/IQR based)
**Status**: Not currently used, but available
**Use**: If StandardScaler is too sensitive to outliers

### Option 4: Separate Outlier Flags
**Method**: Create binary features indicating outlier periods
**Benefit**: Model can learn "normal" vs "extreme" periods
**Example**: `is_crisis_period`, `is_high_volume_day`

---

## Important Notes

1. **Outliers are Mostly Valid**: 
   - Financial crises, IPOs, earnings = real extreme events
   - Not data errors

2. **Outliers are Informative**:
   - VIX outliers during 2008 = market stress signals
   - Volume outliers during IPO = expected behavior
   - Price outliers = growth over time

3. **For Modeling**:
   - Consider keeping outliers (they're informative)
   - Or create separate features for outlier periods
   - Use robust methods if outliers cause issues

---

## Files Generated

- `outlier_detection_summary.csv`: Complete summary of outliers per column
- Detection methods: Z-Score and IQR
- Examples provided for each major outlier type

---

**Report Generated**: Based on analysis of `integrated_prepared_data.csv`
**Total Rows Analyzed**: 8,720
**Total Columns Analyzed**: 28 numeric columns

