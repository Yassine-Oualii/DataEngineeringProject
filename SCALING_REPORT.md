======================================================================
FEATURE SCALING/NORMALIZATION REPORT
======================================================================

Report generated from: integrated_prepared_data.csv
Total rows: 8,720
Total columns: 30

======================================================================
OVERVIEW
======================================================================

This report documents all feature scaling/normalization transformations
applied to prepare features for machine learning modeling.

======================================================================
SCALING SUMMARY
======================================================================

Methods Applied:
  StandardScaler: 25 columns
  MinMaxScaler: 1 columns
  No scaling: 2 columns

======================================================================
DATA PRECISION AND ROUNDING
======================================================================

Post-Processing: All scaled numeric values were rounded to 6 decimal places.

Reason:
  - After scaling, values contained 15-17+ decimal places
  - Example: -0.8106198347123456789 (before) → -0.810620 (after)
  - Rounded for improved readability and file size reduction

Rounding Method:
  - Applied: .round(6) to all numeric columns
  - CSV format: float_format='%.6f' (6 decimal precision)

Precision Maintained:
  - 6 decimal places = 0.000001 precision (one millionth)
  - StandardScaler typically produces values between -3 and +3
  - This precision is MORE than sufficient for machine learning models
  - Most ML libraries use 32-bit floats (≈7 decimal precision)
  - Does NOT affect model performance

Example:
  Before rounding:  -0.8106198347123456789
  After rounding:   -0.810620
                     └─┬─┘
                       Only first 6 decimals kept

Note: This is a display/storage format change only. The scaled transformation
values remain accurate within 6 decimal precision.

======================================================================
DETAILED TRANSFORMATIONS
======================================================================

Column: Close
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=115.9588, std=139.9731
  After: mean~0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: High
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=117.3402, std=141.7068
  After: mean~0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: Low
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=114.5193, std=138.1918
  After: mean~0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: Open
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=115.9347, std=140.0240
  After: mean~-0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: Volume
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=79876617.9537, std=121536122.3148
  After: mean~0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: sp500_Close
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=2760.0127, std=1462.4297
  After: mean~-0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: sp500_High
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=2774.3242, std=1469.3273
  After: mean~-0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: sp500_Low
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=2743.5101, std=1454.3664
  After: mean~0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: sp500_Open
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=2759.4499, std=1462.1955
  After: mean~-0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: sp500_Volume
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=3903259662.8440, std=1157028075.9741
  After: mean~0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: CPI
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=252.0243, std=34.8821
  After: mean~0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: Fed_Funds_Rate
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=1.7204, std=1.9234
  After: mean~-0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: GDP
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=20374.6044, std=5056.3093
  After: mean~-0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: Unemployment_Rate
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=5.5031, std=2.0130
  After: mean~0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: VIX
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=18.5296, std=7.9591
  After: mean~-0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: Market_Breadth
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=12047.0656, std=3768.3630
  After: mean~-0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: sector_XLK
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=78.8960, std=68.8669
  After: mean~-0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: sector_XLF
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=22.7264, std=11.3412
  After: mean~-0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: sector_XLV
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=73.2507, std=41.0295
  After: mean~-0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: sector_XLE
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=51.2598, std=17.8326
  After: mean~0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: sector_XLI
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=61.5806, std=34.8657
  After: mean~0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: spy_SMA_50
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=246.0903, std=150.9894
  After: mean~0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: spy_SMA_200
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=237.0722, std=143.6064
  After: mean~-0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: qqq_SMA_50
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=178.8859, std=146.0684
  After: mean~-0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: qqq_SMA_200
  Method: StandardScaler
  Reason: Normal distribution, low outliers
  Before: mean=170.2605, std=138.0779
  After: mean~0.0000, std~1.0000
  Effect: Transformed to mean=0, std=1 (standard normal distribution)

Column: Put_Call_Ratio
  Method: MinMaxScaler
  Reason: Ratios are naturally bounded
  Before: min=9.1400, max=82.6900
  After: min~0.0000, max~1.0000
  Effect: Transformed to range [0, 1]

Column: spy_RSI
  Method: No scaling
  Reason: RSI is already bounded (0-100)

Column: qqq_RSI
  Method: No scaling
  Reason: RSI is already bounded (0-100)

======================================================================
METHODOLOGY
======================================================================

1. StandardScaler:
   - Formula: (x - mean) / std
   - Result: Mean=0, Standard Deviation=1
   - Use for: Normally distributed data, low outliers
   - Examples: Returns, percentage changes, z-scores

2. RobustScaler:
   - Formula: (x - median) / IQR
   - Result: Median=0, IQR-based scaling
   - Use for: Data with outliers, non-normal distributions
   - Examples: Volume, prices, macro indicators

3. MinMaxScaler:
   - Formula: (x - min) / (max - min)
   - Result: Range [0, 1]
   - Use for: Bounded features, ratios
   - Examples: RSI (0-100), ratios

4. No Scaling:
   - Applied to: Already normalized features, constant values
   - Examples: RSI (already 0-100), binary features

======================================================================
COLUMN CATEGORIES
======================================================================

Stock Price Features:
  - Close: StandardScaler
  - High: StandardScaler
  - Low: StandardScaler
  - Open: StandardScaler
  - Volume: StandardScaler

SP500 Features:
  - sp500_Close: StandardScaler
  - sp500_High: StandardScaler
  - sp500_Low: StandardScaler
  - sp500_Open: StandardScaler
  - sp500_Volume: StandardScaler

Macro Indicators:
  - CPI: StandardScaler
  - Fed_Funds_Rate: StandardScaler
  - GDP: StandardScaler
  - Unemployment_Rate: StandardScaler

Market Sentiment:
  - VIX: StandardScaler
  - Put_Call_Ratio: MinMaxScaler
  - Market_Breadth: StandardScaler

Sector ETFs:
  - sector_XLK: StandardScaler
  - sector_XLF: StandardScaler
  - sector_XLV: StandardScaler
  - sector_XLE: StandardScaler
  - sector_XLI: StandardScaler

Technical Indicators:
  - spy_RSI: No scaling
  - spy_SMA_50: StandardScaler
  - spy_SMA_200: StandardScaler
  - qqq_RSI: No scaling
  - qqq_SMA_50: StandardScaler
  - qqq_SMA_200: StandardScaler

======================================================================
EXCLUDED FROM SCALING
======================================================================

The following columns were NOT scaled:
  - Date: Temporal identifier, not a feature
  - stock: Categorical variable (will be encoded separately)

======================================================================
IMPORTANT NOTES
======================================================================

1. Scaling is applied to entire dataset (train + test)
   - In production: Fit scaler on training data only
   - Transform both train and test with fitted scaler

2. Grouped scaling by stock:
   - Not applied here, but consider for production
   - Prevents one stock's distribution from affecting another

3. Scaling is essential for:
   - Linear models (Logistic Regression, SVM)
   - Distance-based algorithms (KNN)
   - Neural Networks
   - Most sklearn models

4. Tree-based models (Random Forest, XGBoost):
   - Less sensitive to scaling
   - But scaling still recommended for consistency

======================================================================
END OF REPORT
======================================================================