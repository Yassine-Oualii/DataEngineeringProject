# Data Integration Plan

## Target Structure

**One combined dataset** where each row represents:
- (Stock, Date) pair
- All engineered features
- Label (y = 1 if stock outperformed SP500, else 0)

## Data Flow

```
Raw CSVs → Load & Parse → RAW DATA INTEGRATION → Feature Engineering → Labels → Final Dataset
```

## Integration Steps

### Step 1: Load & Parse All Raw Data
Load all CSV files and fix MultiIndex issues:
- **Stock prices**: GOOGL_raw.csv, META_raw.csv (Date, Open, High, Low, Close, Volume)
- **Benchmark**: ^GSPC_raw.csv (Date, Open, High, Low, Close, Volume)
- **Macro data**: CPI_fred.csv, Fed_Funds_Rate_fred.csv, GDP_fred.csv, Unemployment_Rate_fred.csv
- **Market indicators**: vix_term_structure.csv, put_call_ratio.csv, market_breadth.csv
- **Sector ETFs**: sector_XLK.csv, sector_XLF.csv, etc.

### Step 2: RAW DATA INTEGRATION
Create one integrated raw dataset with all data sources aligned by date:

**2a. Stock Data Integration**
- Combine GOOGL, META into one DataFrame
- Add `stock` column identifier
- Stack/union: [stock, date, Open, High, Low, Close, Volume]

**2b. Add SP500 Data**
- Keep SP500 separate (not stacked with stocks)
- Will use for comparison/features

**2c. Macro/Market Data Merge**
- Forward-fill monthly macro data to daily
- Inner join all market indicators by Date
- Result: One master dataset with columns:
  - `stock`, `date`
  - Stock OHLCV columns
  - SP500 OHLCV columns (prefixed as `sp500_Close`, etc.)
  - Macro columns (`CPI`, `Fed_Funds_Rate`, etc.)
  - Market columns (`VIX`, `Put_Call_Ratio`, etc.)

**Output**: `integrated_raw_data.csv` or DataFrame ready for feature engineering

### Step 3: Feature Engineering (on integrated raw data)
Now compute features from the integrated dataset:
- Stock features: daily_return, rolling returns, volatility, MA ratios, etc.
- Relative features: stock_return vs sp500_return, stock_vol vs sp500_vol
- Macro features: CPI_change (month-over-month), Fed Funds rate change
- Market features: VIX levels, sector performance

### Step 4: Label Construction
- Compute forward 21-day returns for each stock and SP500
- Create binary label: y = 1 if stock_fwd_ret > sp500_fwd_ret, else 0
- Add label column to feature dataset

### Step 5: Final Cleanup
- Remove unnecessary raw columns (keep only features + label)
- Sort by Date, then Stock
- Export to `ml_dataset.csv`

## Integration Examples

### Example 1: Stock Price Features
```
Input: GOOGL_raw.csv
- Date: 2020-01-15
- Close: 150.50
- High: 152.00
- Low: 149.00
- Volume: 1000000

Output Features:
- daily_return: 0.02
- rolling_ret_5d: 0.05
- rolling_ret_21d: 0.12
- volatility_21d: 0.015
- ma20_ratio: 1.05
- ma50_ratio: 1.10
- price_range: 0.02
- volume_zscore: 0.85
```

### Example 2: Macro Data Integration
```
Input: CPI_fred.csv (monthly)
- 2020-01-01: 250.0
- 2020-02-01: 251.0

After forward-fill to daily:
- 2020-01-15: 250.0  (fills from Jan 1)
- 2020-01-20: 250.0  (fills from Jan 1)
- 2020-02-05: 251.0  (fills from Feb 1)

Merge to stock data:
- GOOGL 2020-01-15: [features...] + CPI_change: 0.0
- GOOGL 2020-02-05: [features...] + CPI_change: 0.004
```

### Example 3: Date Alignment
```
Stock dates: [2020-01-15, 2020-01-16, 2020-01-20]  (skips weekends)
VIX dates:   [2020-01-15, 2020-01-16, 2020-01-17, 2020-01-20]

Merge: Keep only common trading days (inner join)
Result: [2020-01-15, 2020-01-16, 2020-01-20]
```

### Example 4: Multi-Stock Integration
```
GOOGL features:
- 2020-01-15, GOOGL, [features...], label=1
- 2020-01-16, GOOGL, [features...], label=0

META features:
- 2020-01-15, META, [features...], label=1
- 2020-01-16, META, [features...], label=1

Final combined:
- 2020-01-15, GOOGL, [features...], label=1
- 2020-01-15, META, [features...], label=1
- 2020-01-16, GOOGL, [features...], label=0
- 2020-01-16, META, [features...], label=1
```

## File Structure

### Option A: One Final CSV (Recommended)
```
ml_dataset.csv
- stock (GOOGL, META)
- date
- feature1, feature2, ..., featureN
- label (0 or 1)
```

### Option B: Separate Feature Files (Alternative)
```
features_googl.csv
features_meta.csv
labels_googl.csv
labels_meta.csv
```

**Recommendation: Option A** - easier for modeling, single source of truth

## Integration Challenges

1. **MultiIndex CSV format** - Need to parse correctly
2. **Date alignment** - Different start dates (GOOGL 2004, SP500 2000)
3. **Frequency mismatch** - Macro data monthly, stock data daily → forward-fill
4. **Missing dates** - Holidays/weekends → use inner join on trading days
5. **Multi-stock combination** - Need stock identifier column

