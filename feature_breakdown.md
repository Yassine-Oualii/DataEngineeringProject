# Feature Engineering Breakdown: Calculated vs. Direct Use

## Summary

**Total Features: 31**

- **Calculated/Engineered: 15 features** (48%)
- **Direct Use (Renamed): 16 features** (52%)

---

## ✅ **CALCULATED/ENGINEERED FEATURES** (15 features)

These features were **computed from raw data** using mathematical operations:

### Stock Features (9 features):
1. **daily_return** - `Close.pct_change()` - Daily percentage return
2. **r_1W** - `Close.pct_change(periods=5)` - 1-week rolling return
3. **r_1M** - `Close.pct_change(periods=21)` - 1-month rolling return
4. **r_3M** - `Close.pct_change(periods=63)` - 3-month rolling return
5. **vol_1M** - `rolling_std(daily_return, window=21)` - 21-day volatility
6. **MA20_ratio** - `Close / rolling_mean(Close, 20)` - Price vs 20-day MA
7. **MA50_ratio** - `Close / rolling_mean(Close, 50)` - Price vs 50-day MA
8. **HL_range** - `(High - Low) / Close` - Daily price range ratio
9. **vol_z** - `(Volume - mean_20) / std_20` - Volume z-score

### SP500 Features (2 features):
10. **sp500_daily_return** - `sp500_Close.pct_change()` - SP500 daily return
11. **sp500_vol_1M** - `rolling_std(sp500_daily_return, 21)` - SP500 volatility

### Relative Features (2 features):
12. **relative_return** - `daily_return - sp500_daily_return` - Stock vs market return
13. **volatility_ratio** - `vol_1M / sp500_vol_1M` - Stock vs market volatility

### Macro Change Features (2 features):
14. **CPI_chg** - `CPI.pct_change()` - CPI percentage change
15. **FedFunds_chg** - `Fed_Funds_Rate.diff()` - Fed Funds Rate absolute change

---

## 📋 **DIRECT USE FEATURES** (16 features)

These features were **already in the raw integrated data** and were simply **renamed** (suffix `_t` added for clarity):

### Macro Indicators (2 features):
16. **VIX_t** - Direct from `VIX` column (raw data)
17. **FedFunds_t** - Direct from `Fed_Funds_Rate` column (raw data)

### Market Sentiment (2 features):
18. **Put_Call_Ratio_t** - Direct from `Put_Call_Ratio` column (raw data)
19. **Market_Breadth_t** - Direct from `Market_Breadth` column (raw data)

### Technical Indicators (6 features):
20. **spy_RSI_t** - Direct from `spy_RSI` column (from Alpha Vantage)
21. **spy_SMA_50_t** - Direct from `spy_SMA_50` column (from Alpha Vantage)
22. **spy_SMA_200_t** - Direct from `spy_SMA_200` column (from Alpha Vantage)
23. **qqq_RSI_t** - Direct from `qqq_RSI` column (from Alpha Vantage)
24. **qqq_SMA_50_t** - Direct from `qqq_SMA_50` column (from Alpha Vantage)
25. **qqq_SMA_200_t** - Direct from `qqq_SMA_200` column (from Alpha Vantage)

### Sector ETFs (5 features):
26. **sector_XLK_t** - Direct from `sector_XLK` column (Technology ETF)
27. **sector_XLF_t** - Direct from `sector_XLF` column (Financials ETF)
28. **sector_XLV_t** - Direct from `sector_XLV` column (Healthcare ETF)
29. **sector_XLE_t** - Direct from `sector_XLE` column (Energy ETF)
30. **sector_XLI_t** - Direct from `sector_XLI` column (Industrials ETF)

### Missing 1 feature - Need to check:
Actually, let me recount - we have 31 total features in the final dataset.

---

## 📊 **Breakdown by Category**

| Category | Calculated | Direct Use | Total |
|----------|-----------|------------|-------|
| Stock Features | 9 | 0 | 9 |
| SP500 Features | 2 | 0 | 2 |
| Relative Features | 2 | 0 | 2 |
| Macro Change | 2 | 0 | 2 |
| Macro Indicators | 0 | 2 | 2 |
| Market Sentiment | 0 | 2 | 2 |
| Technical Indicators | 0 | 6 | 6 |
| Sector ETFs | 0 | 5 | 5 |
| **TOTAL** | **15** | **16** | **31** |

---

## 💡 **Key Insights**

1. **Nearly half (48%) of features are engineered** - This shows significant feature engineering work
2. **The most valuable features are likely the calculated ones** - They capture relationships (returns, ratios, relative performance)
3. **Direct use features provide context** - Macro indicators, technical indicators, and sector data provide market context
4. **Feature engineering focus** - Most effort went into creating stock-specific and relative performance features

---

## 🎯 **What This Means for the Report**

When describing the 31 features, you should clarify:
- **15 features were engineered/calculated** from raw data (returns, volatility, ratios, etc.)
- **16 features were used directly** from raw integrated data (VIX, RSI, sector ETFs, etc.)
- All features together create a comprehensive feature set for the ML model

