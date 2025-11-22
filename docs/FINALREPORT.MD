# Stock Market Outperformance Prediction: Data Science Report

**Course:** Data Science Fundamentals  
**Date:** November 2, 2025  
**Subject:** Stock Market Prediction Using Machine Learning

---

## Table of Contents

1. [Problem Definition and Task Overview](#a-problem-definition)
2. [Data Integration](#c-data-integration)
3. [Data Preparation](#d-data-preparation)
4. [Conclusion](#conclusion)

---

## A. Problem Definition and Task Overview

### 1.1 Main Topic

This project focuses on predicting whether individual stocks will outperform the S&P 500 index over a future time horizon, providing actionable insights for investment decision-making. The ability to predict relative stock performance is crucial for portfolio management and investment strategy development.

### 1.2 Prediction Task

**Objective:** Predict whether a given stock will outperform the S&P 500 benchmark over the next 21 trading days (approximately one month).

**Task Type:** This is a **supervised binary classification problem**.

**Target Variable Definition:**

$$y_t = \begin{cases} 1 & \text{if } r_{t,t+21}^{\text{stock}} > r_{t,t+21}^{\text{S\&P 500}} \\ 0 & \text{otherwise} \end{cases}$$

where:
- $r_{t,t+21}$ represents the percentage return over the next 21 trading days
- $y = 1$ indicates the stock outperforms the S&P 500 (positive class)
- $y = 0$ indicates the stock underperforms or matches the S&P 500 (negative class)

### 1.3 Classification vs. Regression

**This is a classification task, not regression, for the following reasons:**

1. **Discrete Output:** The model outputs one of two discrete classes (outperform or underperform), not a continuous value
2. **Decision-Oriented:** The goal is to make binary investment decisions (buy/hold vs. avoid)
3. **Benchmark-Relative:** We care about relative performance ranking, not absolute return magnitude
4. **Evaluation Metrics:** Success is measured by classification metrics (accuracy, precision, recall, F1-score) rather than regression metrics (MSE, RMSE)

### 1.4 Input Features

The model utilizes **31 engineered features** derived from multiple data sources:

| Feature Category | Description | Examples |
|-----------------|-------------|----------|
| **Momentum Indicators** | Rolling returns capturing price trends | 1-week, 1-month, 3-month returns |
| **Volatility Metrics** | Risk and price fluctuation measures | 21-day rolling standard deviation |
| **Technical Ratios** | Price-based technical indicators | MA20, MA50 ratios, daily range, volume z-scores |
| **Relative Performance** | Stock vs. market comparison | Stock returns vs. S&P 500 returns |
| **Macroeconomic Variables** | Economic context indicators | VIX, Federal Funds Rate, CPI, unemployment |
| **Market Sentiment** | Investor behavior indicators | Put/call ratio, market breadth |
| **Sector Performance** | Sector-level market trends | XLK, XLF, XLV, XLE, XLI ETF prices |
| **Technical Indicators** | Market-wide technical metrics | SPY/QQQ RSI, SMA_50, SMA_200 |

**Key Design Principle:** All features are computed using only information available up to the prediction date to prevent data leakage. Each observation represents a unique (stock, date) pair.

---

## C. Data Integration

### 2.1 Integration Process Overview

The project integrated multiple heterogeneous data sources with different temporal granularities, coverage periods, and reporting frequencies. This integration was essential to create a comprehensive feature set capturing stock-specific, market-wide, and macroeconomic factors.

**Primary Data Sources:**

| Data Source | Granularity | Coverage | Variables |
|------------|-------------|----------|-----------|
| Individual Stock Data | Daily | 2004-2024 | OHLCV (Open, High, Low, Close, Volume) |
| S&P 500 Index | Daily | 2000-2024 | Market benchmark OHLCV |
| Macroeconomic Indicators | Monthly/Quarterly | 2000-2024 | CPI, GDP, unemployment, Fed Funds Rate |
| Market Sentiment | Daily | 2000-2024 | VIX, put/call ratio, market breadth |
| Sector ETFs | Daily | 2000-2024 | Five sector ETF prices |
| Technical Indicators | Daily | 2000-2024 | RSI, moving averages for SPY/QQQ |

### 2.2 Integration Challenges Addressed

#### Challenge 1: Temporal Alignment

**Problem:** Different data sources had varying start dates and coverage periods.

**Data Source Start Dates:**
- S&P 500 index: January 3, 2000
- GOOGL stock: August 19, 2004 (IPO date)
- META stock: Different IPO date
- Macroeconomic data: Varying availability

**Solution:** Implemented date-based left joins ensuring all stocks are matched only to dates where both stock and market data exist. This approach respects the natural temporal boundaries of each dataset.

**Result:** 
- Common dates for GOOGL and S&P 500: 5,336 trading days
- S&P 500-only dates (pre-GOOGL IPO): 1,162 days (excluded from analysis)
- Zero date mismatches in final integrated dataset

---

#### Challenge 2: Missing Trading Days

**Problem:** Markets are closed on weekends, holidays, and exceptional circumstances (e.g., September 11, 2001).

**Analysis Results:**
- **GOOGL:** 196 missing trading days (primarily holidays)
- **S&P 500:** 242 missing trading days (holidays + September 11-14, 2001 market closure)

**Examples of Expected Missing Dates:**
- Labor Day (September 6)
- Thanksgiving (November 25)
- Christmas Day (December 25)
- New Year's Day (January 1)
- September 11-14, 2001 (market closure following terrorist attacks)

**Solution:** These missing days were intentionally preserved as gaps rather than imputed. Markets were genuinely closed, so no trading data should exist for these dates.

**Validation:** Cross-referenced missing dates with official NYSE/NASDAQ holiday calendars to confirm all gaps were legitimate.

---

#### Challenge 3: Data Frequency Mismatch

**Problem:** Different indicators had different reporting frequencies, creating temporal misalignment.

**Frequency Analysis:**

| Data Type | Frequency | Examples | Reporting Pattern |
|-----------|-----------|----------|-------------------|
| Daily | Every trading day | Stock prices, VIX, sector ETFs | 252 days/year |
| Monthly | First business day | CPI, unemployment rate | 12 reports/year |
| Quarterly | First month of quarter | GDP | 4 reports/year |

**Solution:** Applied forward-fill strategy within reporting periods, ensuring no future information leakage:

1. Monthly data: Forward-filled until next monthly report
2. Quarterly data: Forward-filled until next quarterly report
3. Daily data: No filling required (naturally complete)

**Example Timeline (CPI):**
```
Aug 1, 2024: CPI = 296.50 → Forward-fill to all August dates
Sep 1, 2024: CPI = 297.10 → Forward-fill to all September dates
Oct 1, 2024: CPI = 297.80 → Forward-fill to all October dates
```

This approach ensures that on any given date, we use only the most recent available macroeconomic data, mimicking real-world information availability.

---

### 2.3 Integration Examples

#### Example 1: Stock-to-Market Integration

**Scenario:** Combining individual stock data with market-wide indicators for a single date.

```
Date: August 19, 2004 (GOOGL IPO Day)

Stock-Specific Data (GOOGL):
  - Close: $2.4938
  - High: $2.5619
  - Low: $2.4256
  - Open: $2.5000
  - Volume: 893,181,924 shares

Market-Wide Data (Shared by All Stocks):
  - S&P 500 Close: $1,091.23
  - VIX: 15.48
  - Fed Funds Rate: 1.43%
  - CPI: 189.80 (filled from September)

Integration Result: Single row combining stock-specific values with 
market context, enabling the model to learn how GOOGL performed 
relative to market conditions on its IPO day.
```

**Key Insight:** This integration allows the model to learn that GOOGL's performance should be evaluated in the context of overall market conditions (low VIX = stable market, low interest rates = favorable conditions).

---

#### Example 2: Multi-Stock Same-Date Integration

**Scenario:** Multiple stocks share identical market data on the same date but have different stock-specific values.

```
Date: September 23, 2024

GOOGL Row:
  - Stock: GOOGL
  - Close: $163.57
  - Volume: 25,482,700
  - S&P 500 Close: $5,718.57
  - VIX: 14.23
  - sector_XLK: $226.84

META Row:
  - Stock: META
  - Close: $562.64
  - Volume: 12,830,700
  - S&P 500 Close: $5,718.57
  - VIX: 14.23
  - sector_XLK: $226.84

Integration Result: Two separate rows with:
  - Different stock-specific values (Close, Volume)
  - Identical market-wide values (S&P 500, VIX, sectors)
```

**Key Insight:** This structure enables the model to learn cross-sectional patterns—how different stocks respond to the same market conditions.

---

#### Example 3: Macroeconomic Data Integration with Temporal Gap Handling

**Scenario:** Integrating quarterly GDP data with daily stock data.

```
Date Range: August 2004 (GOOGL IPO month)

Daily Stock Data:
  - Aug 19, 2004: GOOGL Close = $2.4938, GDP = NULL
  - Aug 20, 2004: GOOGL Close = $2.6930, GDP = NULL
  - Aug 23, 2004: GOOGL Close = $2.6620, GDP = NULL
  - ... (40 more trading days with NULL GDP)
  - Oct 1, 2004: GDP reported = $12,527.21 billion

Integration Approach:
  Step 1: Forward-fill within stock groups
  Step 2: Backward-fill to handle initial NULLs

Final Result:
  - Aug 19, 2004: GOOGL Close = $2.4938, GDP = $12,527.21 (filled)
  - Aug 20, 2004: GOOGL Close = $2.6930, GDP = $12,527.21 (filled)
  - Oct 1, 2004: GOOGL Close = $3.8740, GDP = $12,527.21 (original)
```

**Justification:** GDP changes slowly (quarterly). Using the next quarter's value for the previous quarter introduces minimal error and is more accurate than leaving NULLs or using interpolation.

---

### 2.4 Functional Dependencies in the Dataset

Functional dependencies (FDs) describe deterministic relationships between attributes. Understanding these relationships is critical for ensuring data integrity, avoiding redundancy, and designing efficient database schemas.

#### 2.4.1 Candidate Key Analysis

**Definition:** A candidate key is a minimal set of attributes that uniquely identifies each row.

**Analysis:**

```
Candidate Key: (stock, Date)

Validation:
  - Total unique (stock, Date) pairs: 8,720
  - Total rows: 8,720
  - Conclusion: ✓ No duplicates; (stock, Date) is a valid candidate key

Alternative Key Attempts:
  - Date alone: 5,336 unique values out of 8,720 rows
    → FAILS: Multiple stocks exist per date
  
  - Stock alone: 2 unique values out of 8,720 rows
    → FAILS: Multiple dates exist per stock
```

**Conclusion:** `(stock, Date)` is the primary key, uniquely identifying each observation in the dataset.

---

#### 2.4.2 Identified Functional Dependencies

**FD1: Stock-Specific Price Dependency**

```
(stock, Date) → {Close, High, Low, Open, Volume}
```

**Interpretation:** For a given stock on a specific date, there exists exactly one set of OHLCV values. This is the fundamental relationship defining stock price data.

**Validation:** ✓ Confirmed across all 8,720 rows with no violations.

**Example:**
```
(stock=GOOGL, Date=2004-08-19) determines:
  - Close = $2.4938
  - High = $2.5619
  - Low = $2.4256
  - Open = $2.5000
  - Volume = 893,181,924

This combination uniquely identifies one trading record.
```

---

**FD2: Market Benchmark Dependency**

```
Date → {sp500_Close, sp500_High, sp500_Low, sp500_Open, sp500_Volume}
```

**Interpretation:** For any given date, all stocks share identical S&P 500 values because the market benchmark is the same for everyone on the same trading day.

**Validation:** ✓ Verified by checking all stocks on multiple dates.

**Example:**
```
Date = August 19, 2004

All stocks (GOOGL, META, etc.) on this date have:
  - sp500_Close = $1,091.23
  - sp500_High = $1,094.28
  - sp500_Low = $1,088.77
  - sp500_Open = $1,092.54
  - sp500_Volume = 1,445,620,000

This data is duplicated across stocks but functionally determined by Date.
```

**Implications for Database Design:** In a normalized database, S&P 500 data would be stored in a separate table with Date as the key to avoid redundancy.

---

**FD3: Macroeconomic Indicator Dependency**

```
Date → {CPI, Fed_Funds_Rate, GDP, Unemployment_Rate}
```

**Interpretation:** Macroeconomic indicators are country-wide statistics that apply equally to all stocks on the same date.

**Validation:** ✓ Confirmed by checking multiple dates and stocks.

**Example:**
```
Date = September 1, 2004

For all stocks (GOOGL, META):
  - CPI = 189.80
  - Fed_Funds_Rate = 1.43%
  - GDP = $12,527.21 billion
  - Unemployment_Rate = 5.40%

These values are identical across all stocks because they represent 
national economic conditions, not stock-specific attributes.
```

**Note:** One violation was detected where CPI had multiple values for the same date, indicating a data quality issue that was resolved during data cleaning.

---

**FD4: Market Sentiment Dependency**

```
Date → {VIX, Put_Call_Ratio, Market_Breadth}
```

**Interpretation:** Market sentiment indicators reflect overall market conditions on a given day and are shared by all stocks.

**Validation:** ✓ Verified across all dates.

**Example:**
```
Date = October 7, 2008 (Financial Crisis Peak)

All stocks on this date share:
  - VIX = 53.68 (extreme fear)
  - Put_Call_Ratio = 16.96
  - Market_Breadth = -0.34 (broad market decline)

These values capture market-wide panic during the crisis, affecting 
all stocks simultaneously.
```

---

**FD5: Sector Performance Dependency**

```
Date → {sector_XLK, sector_XLF, sector_XLV, sector_XLE, sector_XLI}
```

**Interpretation:** Sector ETF prices represent sector-wide performance and are identical for all stocks on the same date, regardless of which sector the stock belongs to.

**Validation:** ✓ Confirmed across all dates and stocks.

**Example:**
```
Date = September 23, 2024

All stocks (GOOGL, META) share:
  - sector_XLK (Technology) = $226.84
  - sector_XLF (Financials) = $43.92
  - sector_XLV (Healthcare) = $142.76
  - sector_XLE (Energy) = $91.34
  - sector_XLI (Industrials) = $134.52

These provide sector context for evaluating relative performance.
```

---

**FD6: Technical Indicator Dependency**

```
Date → {spy_RSI, spy_SMA_50, spy_SMA_200, qqq_RSI, qqq_SMA_50, qqq_SMA_200}
```

**Interpretation:** Market-wide technical indicators are computed from index data (SPY = S&P 500 ETF, QQQ = NASDAQ ETF) and apply to all stocks on the same date.

**Validation:** ✓ Verified across all observations.

**Example:**
```
Date = July 15, 2024

All stocks share:
  - spy_RSI = 58.32 (moderate momentum)
  - spy_SMA_50 = $542.18
  - spy_SMA_200 = $495.67
  - qqq_RSI = 62.45 (slightly overbought)
  - qqq_SMA_50 = $475.23
  - qqq_SMA_200 = $420.89
```

---

#### 2.4.3 Summary of Functional Dependencies

```
Primary Key: (stock, Date)

Stock-Specific Dependencies:
  (stock, Date) → {Close, High, Low, Open, Volume}

Market-Wide Dependencies (Shared Across All Stocks):
  Date → {sp500_Close, sp500_High, sp500_Low, sp500_Open, sp500_Volume}
  Date → {CPI, Fed_Funds_Rate, GDP, Unemployment_Rate}
  Date → {VIX, Put_Call_Ratio, Market_Breadth}
  Date → {sector_XLK, sector_XLF, sector_XLV, sector_XLE, sector_XLI}
  Date → {spy_RSI, spy_SMA_50, spy_SMA_200, qqq_RSI, qqq_SMA_50, qqq_SMA_200}

Redundancy Implication:
  - Market-wide data is duplicated across all stocks on the same date
  - This duplication is intentional for machine learning (each row is a 
    complete feature vector)
  - In a production database, normalized design would store market-wide 
    data in separate tables
```

---

## D. Data Preparation

### 3.1 Handling Missing Data

#### 3.1.1 Overview of Missing Data Strategy

Missing data occurred primarily in two scenarios:

1. **Macroeconomic indicators:** Monthly and quarterly data with gaps between reporting periods
2. **Initial rows:** Insufficient historical data for computing rolling window features (e.g., 3-month returns require 63 days of history)

**Overall Approach:**

| Scenario | Strategy | Rationale |
|----------|----------|-----------|
| Macroeconomic gaps | Forward-fill + Backward-fill | Indicators change slowly; use most recent known value |
| Insufficient history | Row deletion | Cannot compute features without sufficient data |
| Trading day gaps | No imputation | Markets genuinely closed; gaps are valid |

---

#### 3.1.2 Macroeconomic Data Imputation Examples

The following examples demonstrate how missing macroeconomic data was handled using forward-fill followed by backward-fill (bfill) within stock groups.

---

**Example 1: CPI (Consumer Price Index)**

**Original State:**
```
Date: August 19, 2004 (GOOGL IPO day)
CPI: NULL (no CPI reported yet for August)
```

**Filling Process:**

Step 1: Identify reporting pattern
- CPI is reported monthly on the first business day of each month
- August 2004 CPI: Not yet reported
- Next available CPI: September 1, 2004 = 189.80

Step 2: Apply backward fill
- Propagate September's CPI (189.80) backward to all August dates
- Result: August 19, 2004 → CPI = 189.80

**Final Result:**
```
Date: August 19, 2004
CPI: 189.80 (filled from September 1, 2004)
```

**Justification:** 
- CPI changes gradually month-to-month (typically < 0.3% monthly)
- Using next month's value for previous month introduces minimal error
- Alternative approaches (mean imputation, interpolation) would be less accurate because CPI follows a trending pattern
- This approach mimics real-world scenario: investors in August would use July's CPI (if available) or wait for September's report

**Impact on Model:** Enables model to learn relationships between inflation levels and stock performance without discarding valuable observations.

---

**Example 2: GDP (Gross Domestic Product)**

**Original State:**
```
Date: August 19, 2004 (GOOGL IPO day)
GDP: NULL (Q3 2004 GDP not yet reported)
```

**Filling Process:**

Step 1: Identify reporting pattern
- GDP is reported quarterly (Q1: Apr, Q2: Jul, Q3: Oct, Q4: Jan)
- August 19, 2004 falls in Q3 2004
- Q3 2004 GDP reported: October 1, 2004 = $12,527.21 billion
- Time gap: 43 days forward

Step 2: Apply backward fill
- Propagate Q3 GDP backward to all August-September dates
- Result: August 19, 2004 → GDP = $12,527.21 billion

**Final Result:**
```
Date: August 19, 2004
GDP: $12,527.21 billion (filled from October 1, 2004)

Complete Q3 2004 Timeline:
  - Aug 19, 2004: GDP = $12,527.21 (filled)
  - Sep 15, 2004: GDP = $12,527.21 (filled)
  - Oct 1, 2004: GDP = $12,527.21 (original)
```

**Justification:**
- GDP is a slow-moving indicator (quarterly reporting)
- Quarterly changes are typically < 1% in stable economies
- Using next quarter's value for the same quarter is appropriate given the low volatility
- Reflects information lag: investors in August don't have Q3 GDP yet

**Alternative Rejected:** Linear interpolation between Q2 and Q3 would imply smooth GDP growth, which doesn't reflect how GDP is actually reported (discrete quarterly values).

---

**Example 3: Unemployment Rate**

**Original State:**
```
Date: August 19, 2004
Unemployment_Rate: NULL (August rate not yet reported)
```

**Filling Process:**

Step 1: Identify reporting pattern
- Unemployment rate is reported monthly (first Friday of each month)
- August 2004 rate: Not yet reported on August 19
- Next available rate: September 1, 2004 = 5.40%
- Time gap: 13 days forward

Step 2: Apply backward fill
- Propagate September's rate backward to all August dates
- Result: August 19, 2004 → Unemployment_Rate = 5.40%

**Final Result:**
```
Date: August 19, 2004
Unemployment_Rate: 5.40% (filled from September 1, 2004)

Context:
  - July 2004: 5.50%
  - August 2004: 5.40% (filled)
  - September 2004: 5.40% (original)
```

**Justification:**
- Unemployment rate is relatively stable month-to-month
- Monthly changes are typically ≤ 0.2 percentage points in normal conditions
- Short time gap (13 days) minimizes potential error
- Backward filling is more accurate than forward filling (less time lag)

**Impact:** Allows the model to incorporate labor market conditions into predictions without losing early observations.

---

#### 3.1.3 Row Deletion for Insufficient Historical Data

**Problem:** Rolling window features (e.g., 3-month returns, 21-day volatility) require sufficient historical data to compute.

**Analysis:**
- 3-month return = 63 trading days of historical data required
- 21-day volatility = 21 trading days of historical data required
- First 63 days of each stock: Insufficient data to compute all features

**Action Taken:**
- **126 rows removed** (1.4% of original dataset)
- Breakdown: First 63 trading days per stock × 2 stocks = 126 rows
- Final dataset: 8,594 observations (down from 8,720)

**Example:**
```
GOOGL IPO: August 19, 2004
First 63 trading days: Aug 19, 2004 - Nov 10, 2004

Rows Removed:
  - Aug 19, 2004: Cannot compute 3-month return (no history)
  - Aug 20, 2004: Cannot compute 3-month return (1 day history)
  - ...
  - Nov 10, 2004: Cannot compute 3-month return (62 days history)

First Valid Row:
  - Nov 11, 2004: Can compute all features (63+ days history)
```

**Alternative Rejected:** Could have imputed missing feature values with zeros or means, but this would introduce noise and bias model training.

**Impact:** Minimal loss (1.4% of data) in exchange for ensuring all features are validly computed.

---

### 3.2 Outlier Detection

#### 3.2.1 Methodology: Z-Score Method

**Definition:** An outlier is defined as any value whose z-score exceeds 3 standard deviations from the mean.

**Mathematical Formula:**

$$\text{Z-score} = \frac{|x - \mu|}{\sigma}$$

$$\text{Outlier if:} \quad |Z\text{-score}| > 3$$

where:
- $x$ = observed value
- $\mu$ = population mean
- $\sigma$ = population standard deviation

**Characteristics:**
- **Appropriate for:** Approximately normally distributed data
- **Sensitivity:** Captures only the most extreme cases (99.7% of normal data falls within ±3σ)
- **Conservative threshold:** Reduces false positives
- **Limitation:** Sensitive to extreme values in small samples

**Implementation:**
```python
# Applied to each numeric column independently
for column in numeric_columns:
    mean = column.mean()
    std = column.std()
    z_scores = (column - mean) / std
    outliers = abs(z_scores) > 3
```

---

#### 3.2.2 Overall Outlier Detection Results

**Summary Statistics:**

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Columns with outliers | 12 out of 31 features | 38.7% of features contain outliers |
| Total outlier instances | 1,889 | Across all features and observations |
| Percentage of dataset | 0.77% | Very low—indicates good data quality |
| Most outliers in | Volume | 892 outlier instances (47.3% of all outliers) |
| Second most | Close price | 267 outlier instances |
| Third most | VIX | 186 outlier instances |

**Columns with No Outliers (19 features):**
- Most technical ratios and moving averages
- Normalized indicators (RSI)
- Relative performance metrics

**Interpretation:** The low overall outlier rate (0.77%) indicates that the dataset is generally well-behaved. Most outliers occur in expected places (volume spikes, extreme price movements, crisis-level VIX).

---

#### 3.2.3 Concrete Outlier Examples

---

**Example 1: Volume Outliers (Extreme Trading Activity)**

**Context:** Trading volume spikes occur during significant market events such as:
- Initial Public Offerings (IPOs)
- Earnings announcements
- Merger/acquisition news
- Market crashes or rallies
- Company scandals or major news

**Top 5 Volume Outliers:**

| Rank | Date | Stock | Volume | Z-Score | Close Price | Context |
|------|------|-------|--------|---------|-------------|---------|
| 1 | 2004-08-19 | GOOGL | 893,181,924 | **6.69** | $2.49 | **IPO Day** |
| 2 | 2004-09-29 | GOOGL | 610,329,060 | 4.36 | $3.26 | Post-IPO surge |
| 3 | 2004-10-21 | GOOGL | 582,996,420 | 4.14 | $3.71 | High activity |
| 4 | 2004-08-20 | GOOGL | 456,686,856 | 3.10 | $2.69 | Day 2 post-IPO |
| 5 | 2004-10-20 | GOOGL | 454,453,092 | 3.08 | $3.49 | High activity |

**Detailed Analysis of Top Outlier:**

```
Date: August 19, 2004 (GOOGL IPO)
Volume: 893,181,924 shares
Z-score: 6.69 standard deviations above mean

Context:
  - GOOGL IPO opening price: $85 (pre-split)
  - Closing price: $100.34 (pre-split) = $2.4938 (post-split)
  - First-day gain: 18%
  - Volume: 27× typical daily volume

Historical Significance:
  - One of the most anticipated IPOs of the 2000s
  - Google's unconventional Dutch auction IPO process
  - Heavy media coverage and investor interest
```

**Interpretation:**
- The most extreme outlier (z-score = 6.69) represents nearly **900 million shares traded** on GOOGL's IPO day
- Normal daily volume for GOOGL: ~30 million shares
- This outlier is **27 times the typical volume**
- **Valid outlier:** Reflects genuine market event (IPO excitement), not a data error
- **Decision:** Retained in dataset—provides valuable information about IPO dynamics

**Why Not Remove?**
- Captures important market behavior during IPOs
- Model can learn that IPO days have unique characteristics
- Removal would lose information about high-volume periods

---

**Example 2: Close Price Outliers (Extreme Stock Valuations)**

**Context:** Stock prices have appreciated significantly over 20+ years. Recent prices represent extreme values relative to historical means, especially for high-performing tech stocks.

**Top 5 Highest Close Price Outliers:**

| Rank | Date | Stock | Close Price | Z-Score | Volume | Percent of Mean | Context |
|------|------|-------|-------------|---------|--------|-----------------|---------|
| 1 | 2024-09-23 | META | **$562.64** | **3.19** | 12,830,700 | 1,119% | All-time high |
| 2 | 2024-09-20 | META | $559.59 | 3.17 | 22,066,800 | 1,113% | Near ATH |
| 3 | 2024-09-19 | META | $557.35 | 3.15 | 15,647,000 | 1,108% | Rally continues |
| 4 | 2024-07-05 | META | $537.70 | 3.01 | 21,354,100 | 1,069% | Summer rally |
| 5 | 2024-09-18 | META | $536.26 | 3.00 | 10,323,500 | 1,066% | Strong momentum |

**Detailed Analysis of Top Outlier:**

```
Date: September 23, 2024
Stock: META
Close Price: $562.64
Z-score: 3.19 standard deviations above mean

Historical Context:
  - META IPO (May 2012): $38
  - All-time low (Nov 2022): $88.09
  - Current price (Sep 2024): $562.64
  - Total appreciation: 1,380% from IPO

Mean Close Price (All Stocks, All Dates): $50